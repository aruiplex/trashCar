# from config.init import cfg
import math
from time import sleep

from numpy import angle
# import serial

# port_pi = serial.Serial(port="/dev/ttyAMA0", baudrate=115200)

# l0 = cfg["car_framework"]["arm"]["l0"]
# l1 = cfg["car_framework"]["arm"]["l1"]
# l2 = cfg["car_framework"]["arm"]["l2"]
# l3 = cfg["car_framework"]["arm"]["l3"]
# l4 = cfg["car_framework"]["arm"]["l4"]
# phi = cfg["car_framework"]["arm"]["phi"]
l0 = 0.218
l1 = 0.222
l2 = 0.15
l3 = 0.23
phi = -math.pi/2


def init_catch():
    return [0x55, 0x55, 0x08, 0x03, 0x01, 0xe8, 0x03, 0x05, 0x00, 0x05]


def do_catch():
    return [0x55, 0x55, 0x08, 0x03, 0x01, 0xe8, 0x03, 0x05, 0x00, 0x07]


def ang_cal(x: float, y: float, z: float):
    a = math.sqrt(x**2 + y**2)-l3*math.cos(phi)
    b = z-l0-l3*math.sin(phi)
    if math.sqrt(a**2+b**2) > (l1+l2) or math.sqrt(a**2+b**2) < (l1-l2):
        raise Exception("can not arrive")

    theta0 = math.atan2(y, x)
    theta2 = - math.acos((a**2 + b**2 - l1**2 - l2**2)/(2*l1*l2))
    t_temp = math.acos((l2**2 - a**2-b**2 - l1**2) /
                       (-2*l1*math.sqrt(a**2+b**2)))
    if theta2 < 0:
        theta1 = math.atan2(b, a)+t_temp
    else:
        theta1 = math.atan2(b, a)-t_temp

    theta3 = phi-theta1-theta2
    return (theta0, theta1, theta2, theta3+0.34)


def __order(cmd: bytes):
    cmd = int(cmd)
    data1 = (cmd >> 8) & 0xff
    data0 = cmd & 0xff
    return data1, data0


def __radian_to_pwm(theta0, theta1, theta2, theta3):
    pwm0 = 1500 + (theta0-math.pi/2) * 2000 / (0.75 * math.pi)
    pwm1 = 1500 + (theta1-math.pi/2) * 2000 / (0.75 * math.pi)
    pwm2 = 1500 + theta2 * 2000 / (0.75 * math.pi)
    pwm3 = 1500 + theta3 * 2000 / (0.75 * math.pi)
    return pwm0, pwm1, pwm2, pwm3


def generate_cmd(theta0, theta1, theta2, theta3, time=2000):
    pwm0, pwm1, pwm2, pwm3 = __radian_to_pwm(theta0, theta1, theta2, theta3)
    cmd = bytearray([0x55, 0x55, 0x11, 0x03, 0x04, *__order(time), 0x00, *__order(
        pwm0), 0x01, *__order(pwm1), 0x02, *__order(pwm2), 0x03, *__order(pwm3)])
    return cmd


if __name__ == "__main__":
    theta0, theta1, theta2, theta3 = ang_cal(0, 0.1, 0.2)
    print(theta0, theta1, theta2, theta3)
    cmd = generate_cmd(theta0, theta1, theta2, theta3)
    print(cmd)
