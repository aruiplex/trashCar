import math
import time

import serial
# from loguru import logger

# from config.init import cfg

wheel0 = serial.Serial(port="/dev/ttyAMA1", baudrate=115200)
wheel1 = serial.Serial(port="/dev/ttyAMA2", baudrate=115200)
wheel2 = serial.Serial(port="/dev/ttyAMA3", baudrate=115200)
wheel3 = serial.Serial(port="/dev/ttyAMA4", baudrate=115200)
wheels = [wheel0, wheel1, wheel2, wheel3]


car_length = 0.29

car_width = 0.24


def move(angle, distance, speed=4000, duration=1):
    """Move car with angle and time in power

    Args:
        angle (float):
        time (float): 
        power (float): 
    """
    distance = distance * 1350 / 0.25
    # Calculate the position of each motor
    dx = distance * math.cos(angle + math.pi/2)
    dy = distance * math.sin(angle + math.pi/2)
    d1 = round(dy - dx)
    d2 = round(dy + dx)
    d3 = round(dy - dx)
    d4 = round(dy + dx)
    # Calculate the speed of each motor
    sx = speed * math.cos(angle + math.pi/2)
    sy = speed * math.sin(angle + math.pi/2)
    s1 = round(sy - sx)
    s2 = round(sy + sx)
    s3 = round(sy - sx)
    s4 = round(sy + sx)
    cmd1 = __generate_cmd(d1, s1)
    cmd2 = __generate_cmd(d2, s2)
    cmd3 = __generate_cmd(d3, s3)
    cmd4 = __generate_cmd(d4, s4)
    cmds = [cmd1, cmd2, cmd3, cmd4]
    __send_cmd(cmds, duration)


def rotate(angle, speed=4000, duration=1):
    """car self rotate,
    counter-clockwise is positive, clockwise is negative

    Args:
        angle: radian format.
        speed: max=4000
    """
    # Calculate the position of each motor
    dis = round(angle * (car_length / 2 + car_width / 2) * 1350 / 0.25)
    d1 = dis
    d2 = -dis
    d3 = -dis
    # The minus sign for motor 2 and 3 is due to their installation direction
    d4 = dis
    # Calculate the speed of each motor
    ang_v = round(speed * (car_length / 2 + car_width / 2) * 1350 / 0.25)
    s1 = ang_v
    s2 = -ang_v
    s3 = -ang_v
    # The minus sign for motor 2 and 3 is due to their installation direction
    s4 = ang_v
    cmd1 = __generate_cmd(d1, s1)
    cmd2 = __generate_cmd(d2, s2)
    cmd3 = __generate_cmd(d3, s3)
    cmd4 = __generate_cmd(d4, s4)
    cmds = [cmd1, cmd2, cmd3, cmd4]
    __send_cmd(cmds, duration)


def __reset():
    return bytearray([0xaa, 0x4d, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff])


def __generate_cmd(d, s) -> bytearray:
    d = int(d)
    s = int(s)
    distance3 = (d >> 24) & 0xff
    distance2 = (d >> 16) & 0xff
    distance1 = (d >> 8) & 0xff
    distance0 = d & 0xff
    speed1 = (s >> 8) & 0xff
    speed0 = s & 0xff
    return bytearray([0xaa, 0x59, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xaa, 0x70, distance3, distance2, distance1, distance0, speed1, speed0, 0xff, 0xff])


def __send_cmd(cmds, duration):
    """Send command to serial port

    Args:
        cmds (bytearray): command
    """
    # reset
    print("sleep")
    time.sleep(duration)
    for cmd, wheel in zip(cmds, wheels):
        wheel.write(__reset())
    print("reset")

    time.sleep(0.02)
    # write command
    for cmd, wheel in zip(cmds, wheels):
        print("write commands")
        wheel.write(cmd)


def __send_cmd_stub(cmds):
    """Send command to serial port

    Args:
        cmds (bytearray): command
    """
    wheels = [0, 1, 2, 3]
    for cmd, wheel in zip(cmds, wheels):
        pass
        # logger.debug(f"{cmd} perform in wheel {wheel}")


if __name__ == "__main__":
    rotate(-math.pi, 4000)
