import math
import time
import serial
from loguru import logger

arm_port = serial.Serial(port="/dev/ttyAMA0", baudrate=9600)

wheel0 = serial.Serial(port="/dev/ttyAMA1", baudrate=115200)
wheel1 = serial.Serial(port="/dev/ttyAMA2", baudrate=115200)
wheel2 = serial.Serial(port="/dev/ttyAMA3", baudrate=115200)
wheel3 = serial.Serial(port="/dev/ttyAMA4", baudrate=115200)
wheels = [wheel0, wheel1, wheel2, wheel3]


car_length = 0.29

car_width = 0.24


def minus_1():
    pass


def minus_2():
    pass


def minus_3():
    pass


def plus_1():
    pass


def plus_2():
    pass


def plus_3():
    pass


def direct():
    pass


move_gap = {
    -1: minus_1,
    -2: minus_2,
    -3: minus_3,
    0: direct,
    1: plus_1,
    2: plus_2,
    3: plus_3,
}


def perform_kick_left():
    return bytearray([0x55, 0x55, 0x05, 0x06, 0x06, 0x01, 0x00])


def perform_block():
    return bytearray([0x55, 0x55, 0x05, 0x06, 0x07, 0x01, 0x00])


def perform_cancel_block():
    return bytearray([0x55, 0x55, 0x05, 0x06, 0x08, 0x01, 0x00])


def perform_right_kick():
    return bytearray([0x55, 0x55, 0x05, 0x06, 0x09, 0x01, 0x00])


def kick():
    # kick
    arm_port.write(perform_kick_left())
    time.sleep(6)
    move(0, 0.2, 4000, 2)
    # time.sleep(4)
    # arm_port.write(perform_block())
    move(-math.pi/2, 1, 4000, 2)
    # time.sleep(2)
    # arm_port.write(perform_cancel_block())
    move(math.pi, 0.2, 4000, 2)
    time.sleep(4)
    arm_port.write(perform_right_kick())
    time.sleep(8)


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
    s1 = abs(round(sy - sx))
    s2 = abs(round(sy + sx))
    s3 = abs(round(sy - sx))
    s4 = abs(round(sy + sx))
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
    dis = round(angle * (car_length / 2 + car_width / 2) * 1350 / 0.325)
    print(f"dis: {hex(dis)}")
    d1 = dis
    d2 = -dis
    d3 = -dis
    # The minus sign for motor 2 and 3 is due to their installation direction
    d4 = dis
    # Calculate the speed of each motor
    ang_v = round(speed)
    print(f"ang_v: {hex(ang_v)}")
    s1 = ang_v
    s2 = ang_v
    s3 = ang_v
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
    # this is a reset sleep, a const
    time.sleep(0.2)
    # write command
    for cmd, wheel in zip(cmds, wheels):
        print("write commands: " + str(cmd))
        wheel.write(cmd)


def first_row():
    """不会再用了
    """
    # collection
    move(0, 1.8, 4000, 0)
    move(math.pi/20, 0.8, 4000, 8)
    move(math.pi/20, 0.8, 4000, 8)
    move(math.pi/20, 0.8, 4000, 8)
    # 入门
    move(-math.pi/25, 0.9, 4000, 8)
    # kick()
    move(math.pi, 0.2, 4000, 8)
    move(0, 0.2, 4000, 8)
    # 向右踢的准备运动
    move(-math.pi/2, 0.6, 4000, 8)
    move(math.pi, 0.2, 4000, 8)
    # kick()
    move(math.pi, 4.2, 4000, 8)


def main():
    first_row()
    # kick()
    # second_row()


if __name__ == "__main__":
    # move(0, 3, 4000, 0)
    # move(0, 4, 4000, 0)
    move(math.pi, 1, 4000, 0)
    move(math.pi, 1, 4000, 4)
    move(math.pi, 1, 4000, 4)
    move(math.pi, 1, 4000, 4)
    # move(0, 4.2, 4000, 0)
    # time.sleep(4)
    # time.sleep(4)
    # main()
    # time.sleep(4)
