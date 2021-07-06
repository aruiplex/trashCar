from time import sleep
import numpy as np
from numpy.lib import math
import pyrealsense2 as rs
from loguru import logger
from main import cfg
import math


class DepthDetector:
    """Get the depth info for the obj 
    and this depth instance should be global unique
    """

    def __init__(self) -> None:
        # Create a context object. This object owns the handles to all connected realsense devices
        self.pipeline = rs.pipeline()
        # Configure streams
        config = rs.config()
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        # Start streaming
        self.pipeline.start(config)
        logger.info("realsense depth detector start")

    def detect(self, point1: np.ndarray, point2: np.ndarray) -> float:
        """
        point1: Upper left corner pixel point.
        point2: Lower right corner pixel point.
        The field of view is 640*480.
        return is the depth of obj;
        """
        while True:
            # This call waits until a new coherent set of frames is available on a device
            # Calls to get_frame_data(...) and get_frame_timestamp(...) on a device will return stable values until wait_for_frames(...) is called
            frames = self.pipeline.wait_for_frames()
            # get three kind of frames to get different info
            depth_frame = frames.get_depth_frame()

            if not depth_frame:
                logger.warning("No depth frame")
                sleep(0.05)
                continue

            sample_matrix_base = np.array(
                cfg["data_filter"]["sampling_method_x"])
            x_zoom, y_zoom = point2 - point1
            """
            `[:, 0:1]` This is a very niubi method to silce array to n chunk, which means,  
            `[:, 0]`: silce the first column to one array
            `[:, 0:1]`: silce the first column to n chunk array.
            ref: https://numpy.org/doc/stable/reference/arrays.indexing.html
            """
            # zoom
            sample_matrix = np.append(
                round(sample_matrix_base[:, 0:1] * x_zoom), round(sample_matrix_base[:, 1:2]*y_zoom), axis=1)
            # bias
            sample_matrix += point1
            # todo: definition but
            depths_raw = np.array([])
            # get samples depth
            for sample in sample_matrix:
                # get spec point from depth frame
                depths_raw = np.append(
                    depths_raw, depth_frame.get_distance(sample[0], sample[1]))
            # get the mean of the filted array to be the final answer for depth
            return np.mean(self._data_filter(depths_raw))

    def _data_filter(self, array: np.ndarray) -> np.ndarray:
        """filter the invalid data
        use n sigma rule in natural distribution
        Args:
            array (np.ndarray): the array need to be filter 

        Returns:
            np.ndarray: the filted array
        """
        # standard deviation
        std = np.std(array)
        mean = np.mean(array)
        # std range = range = (n * -sigma, n * sigma)
        std_range = cfg["data_filter"]["std_range"]
        # filter invalid values,
        return array[(array < mean + std_range*std)
                     & (array > mean - std_range*std)]


class PositionDetector:
    def __init__(self) -> None:
        logger.info("Position Detector start")

    def postition(self, depth: float, point1: np.ndarray, point2: np.ndarray) -> np.ndarray:
        """Get object position base on object bounding box and obj depth 

        Args:
            depth (float): the depth from realsense to object
            point1 (np.ndarray): the upper left point of bounding box of obj
            point2 (np.ndarray): the lower right point of bounding box of obj

        Returns:
            np.ndarray: [angle (phi), x, y]
        """

        """method variables:
        1. n:               the number of pixels from center line. 
        2. side:            True, at left side, 
                            False, at right side.
        3. camera_bias_arm: the distance from camera front of arm.
        """
        x_pixels = cfg["car_framework"]["rgb_camera"]["x_pixels"]
        y_pixels = cfg["car_framework"]["rgb_camera"]["y_pixels"]
        camera_bias_arm = cfg["car_framework"]["camera_bias_arm"]
        n = (point2[0] - point1[0])//2 - x_pixels/2
        if n < 0:
            side = True
        else:
            side = False
        n = abs(n)
        phi = math.atan(n/(x_pixels/2))
        x = depth * math.sin(phi)
        y = depth * math.cos(phi) + camera_bias_arm

        # if the position on the left side
        if side:
            x = -x

        # if the position on the right side
        else:
            phi = 360 - phi

        return np.array([phi, x, y])
