import io
import os
import serial
# json 5 can support comments
import json5
from loguru import logger


def _init_ted() -> serial.Serial:
    """
    Open the serial port
    """
    # aruix: stub
    # return serial.Serial(port="/dev/ttyAMA1", baudrate=115200)
    s = Stub()
    return s._init_ted()


def _read_cfg() -> dict:
    """load config file for globle

    Returns:
        dict: configuration
    """
    with io.open("./cfg.json5") as f:
        logger.info("config load")
        return json5.load(f)


# global configuration
cfg = _read_cfg()


class Stub:
    def _init_ted(self):
        logger.info("init ted")
