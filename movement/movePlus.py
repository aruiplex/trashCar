import math
import numpy as np
import serial
import time
from loguru import logger
# from config.init import cfg

# wheel0 = serial.Serial(port="/dev/ttyAMA2", baudrate=115200)
# wheel1 = serial.Serial(port="/dev/ttyAMA2", baudrate=115200)
# wheel2 = serial.Serial(port="/dev/ttyAMA2", baudrate=115200)
# wheel3 = serial.Serial(port="/dev/ttyAMA2", baudrate=115200)

# wheels = [wheel0, wheel1, wheel2, wheel3]

car_length = 0.29

car_width = 0.24


def move(angle, time, power):
    """Move car with angle and time in power

    Args:
        angle (float):
        time (float): 
        power (float): 
    """
    sx = power * math.cos(angle + math.pi/2)
    sy = power * math.sin(angle + math.pi/2)
    # Calculate the position of each motor
    s1 = round(sy - sx)  # 0.5 is for rounding
    s2 = round(sy + sx)
    s3 = round(sy - sx)
    # The minus sign for motor 1 and 4 is due to their installation direction
    s4 = round(sy + sx)
    __perform([s1, s2, s3, s4], time)


def rotate(time, power):
    """car self rotate,
    counter-clock is positive, clock is negative

    Args:
        time (float): run for a duration
        power (float): power to run
    """
    ang_v = round(power * (car_length / 2 + car_width / 2))
    # Calculate the position of each motor
    s1 = ang_v
    s2 = -ang_v
    s3 = -ang_v
    # The minus sign for motor 2 and 3 is due to their installation direction
    s4 = ang_v
    __perform([s1, s2, s3, s4], time)


def __perform(l, duration):
    l = np.array(l)
    logger.debug(f"MovemenT: {l}")
    cmds = []
    for s in l:
        cmds.append(__generate_cmd(s))
    __send_cmd_stub(cmds)
    # perform time
    time.sleep(duration)
    # reset
    cmds = __reset()
    __send_cmd_stub(cmds)
    logger.debug(f"MovemenT DONE")


def __reset():
    return [0xaa, 0x4d, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff]


def __generate_cmd(s) -> bytearray:
    s = int(s)
    data1 = (s >> 8) & 0xff
    data0 = s & 0xff
    return bytearray([0xaa, 0x4e, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xaa, 0x0c, data1, data0, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff])


def __send_cmd(cmds):
    """Send command to serial port

    Args:
        cmds (bytearray): command
    """
    for cmd, wheel in zip(cmds, wheels):
        wheel.write(cmd)


def __send_cmd_stub(cmds):
    """Send command to serial port

    Args:
        cmds (bytearray): command
    """
    wheels = [0, 1, 2, 3]
    for cmd, wheel in zip(cmds, wheels):
        logger.debug(f"{cmd} perform in wheel {wheel}")


if __name__ == "__main__":
    move(0, 1, 1000)
