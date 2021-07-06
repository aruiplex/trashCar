import io
import serial
import json
from loguru import logger


def init_ted():
    """
    Open the serial port
    """
    return serial.Serial(port="/dev/ttyAMA1", baudrate=115200)


def read_cfg():
    """
    """
    with io.open("./cfg.json") as f:
        logger.info("config load")
        return json.load(f)
