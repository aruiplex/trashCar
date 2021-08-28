"""Run inference with a YOLOv5 model on images, videos, directories, streams

Usage:
    $ python path/to/detect.py --source path/to/img.jpg --weights yolov5s.pt --img 640
"""
from config.init import cfg
if cfg["this"] == "nano":
    import argparse
    import os
    import sys
    import time
    from pathlib import Path

    import cv2
    import numpy as np
    import torch
    import torch.backends.cudnn as cudnn
    from communication.position import Position
    from communication.sender import Sender
    from loguru import logger

    import sense.sense
    from sense.models.experimental import attempt_load
    from sense.utils.datasets import LoadImages, LoadStreams
    from sense.utils.general import (apply_classifier, check_img_size,
                                    check_imshow, check_requirements, colorstr,
                                    increment_path, non_max_suppression,
                                    save_one_box, scale_coords, set_logging,
                                    strip_optimizer, xyxy2xywh)
    from sense.utils.plots import colors, plot_one_box
    from sense.utils.torch_utils import (load_classifier, select_device,
                                        time_synchronized)

    FILE = Path(__file__).absolute()
    sys.path.append(FILE.parents[0].as_posix())  # add yolov5/ to path


    @torch.no_grad()
    def run(weights='../sense/trash.pt',  # model.pt path(s)
            source="0",  # file/dir/URL/glob, 0 for webcam
            imgsz=640,  # inference size (pixels)
            conf_thres=0.6,  # confidence threshold
            iou_thres=0.45,  # NMS IOU threshold
            max_det=1000,  # maximum detections per image
            device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
            view_img=False,  # show results
            save_txt=False,  # save results to *.txt
            save_conf=False,  # save confidences in --save-txt labels
            save_crop=False,  # save cropped prediction boxes
            nosave=False,  # do not save images/videos
            classes=None,  # filter by class: --class 0, or --class 0 2 3
            agnostic_nms=False,  # class-agnostic NMS
            augment=False,  # augmented inference
            update=False,  # update all models
            project='runs/detect',  # save results to project/name
            name='exp',  # save results to project/name
            exist_ok=False,  # existing project/name ok, do not increment
            line_thickness=2,  # bounding box thickness (pixels)
            hide_labels=False,  # hide labels
            hide_conf=False,  # hide confidences
            half=False,  # use FP16 half-precision inference
            ):
        save_img = False  # save inference images

        # Initialize
        set_logging()
        device = select_device(device)
        half &= device.type != 'cpu'  # half precision only supported on CUDA

        # Load model
        model = attempt_load(weights, map_location=device)  # load FP32 model
        stride = int(model.stride.max())  # model stride
        imgsz = check_img_size(imgsz, s=stride)  # check image size
        names = model.module.names if hasattr(
            model, 'module') else model.names  # get class names
        if half:
            model.half()  # to FP16

        logger.info("depth detector start")
        depth_detector = sense.sense.DepthDetector()
        position_detector = sense.sense.PositionDetector()
        attention_detector = sense.sense.AttentionDetector()
        sender = Sender()

        # Set Dataloader
        view_img = check_imshow()
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=imgsz, stride=stride)

        # Run inference
        if device.type != 'cpu':
            model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(
                next(model.parameters())))  # run once
        t0 = time.time()
        for path, img, im0s, vid_cap in dataset:
            img = torch.from_numpy(img).to(device)
            img = img.half() if half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            # Inference
            t1 = time_synchronized()
            pred = model(img, augment=augment)[0]

            # Apply NMS
            pred = non_max_suppression(
                pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
            t2 = time_synchronized()

            # all objects in ONE frame, in the available form
            frame_obj_position = []
            # Process detections / object analysis
            for i, det in enumerate(pred):  # detections per image
                p, s, im0, frame = path[i], f'{i}: ', im0s[i].copy(), dataset.count
                s += '%gx%g ' % img.shape[2:]  # print string
                if len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(
                        img.shape[2:], det[:, :4], im0.shape).round()

                    # Print results
                    for c in det[:, -1].unique():
                        n = (det[:, -1] == c).sum()  # detections per class
                        # add to string
                        s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "

                    # Write results
                    for *xyxy, conf, cls in reversed(det):
                        if save_img or save_crop or view_img:  # Add bbox to image
                            c = int(cls)  # integer class
                            label = None if hide_labels else (
                                names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                            # ----------- base operation to detect obj depth ---------------------------
                            point1, point2 = np.array([int(xyxy[0]), int(
                                xyxy[1])]), np.array([int(xyxy[2]), int(xyxy[3])])
                            # get the distance of the object
                            depth = depth_detector.detect(point1, point2)
                            obj_position = {
                                "point1": point1, "point2": point2, "clz": c, "depth": depth}
                            # add a object postition in a
                            frame_obj_position.append(obj_position)
                            logger.debug(
                                f"point1: {point1}, point2: {point2} label: {label} ({t2 - t1:.3f}s)")
                            # -----------/ base operation to detect obj depth ---------------------------
                            if cfg["mode"] == "dev":
                                # todo: here could be delete in production mode
                                label += f"d: {depth:.3f}m"
                                plot_one_box(xyxy, im0, label=label, color=colors(
                                    c, True), line_thickness=line_thickness)
                                # todo/: here could be delete in production mode
                # ------------------- frame analysis ----------------------
                if frame_obj_position != []:
                    # get the major target
                    # TODO: prime attition has bugs.
                    # obj = attention_detector.attention(frame_obj_position)
                    obj = attention_detector.attention_min(frame_obj_position)
                    # get target position
                    (phi, coord) = position_detector.postition(
                        obj["depth"], obj["point1"], obj["point2"])
                    if cfg["mode"] == "dev":    
                        poi = f"{names[obj['clz']]}({coord[0]:.2f}, {coord[1]:.2f}, {depth:.3f})m"
                        plot_one_box(xyxy, im0, label=poi, color=colors(
                            c, True), line_thickness=2)
                    # calculate the obj position
                    position = Position(
                        names[c] , phi, coordinate=coord).serialization()
                    # port communication
                    sender.send(position)
                    # clean all objects in a frame
                    frame_obj_position = []
                    # Print time (inference + NMS)
                    logger.debug(f'One frame analysis Done.')
                # ------------------- /frame analysis ----------------------

                # Stream results
                if view_img:
                    cv2.imshow(str(p), im0)
                    cv2.waitKey(1)  # 1 millisecond

        # --------------------- end stream ------------------------------------
        print(f'Done. ({time.time() - t0:.3f}s)')


    def main_cv(opt):
        logger.info("detect start")
        run(**opt)
