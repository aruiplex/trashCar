from loguru import logger
import pyrealsense2 as rs


def init_realsense():
    # Create a context object. This object owns the handles to all connected realsense devices
    pipeline = rs.pipeline()
    # Configure streams
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    # Start streaming
    pipeline.start(config)
    logger.info("realsense start")
    return pipeline


def detect_depth(pipeline):
    while True:
        # This call waits until a new coherent set of frames is available on a device
        # Calls to get_frame_data(...) and get_frame_timestamp(...) on a device will return stable values until wait_for_frames(...) is called
        frames = pipeline.wait_for_frames()
        # get three kind of frames to get different info
        depth_frame = frames.get_depth_frame()
        if not depth_frame:
            continue
