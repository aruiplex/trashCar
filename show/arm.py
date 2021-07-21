# import serial


# port_pi = serial.Serial(port="/dev/ttyAMA0", baudrate=115200)

from gpiozero import AngularServo
from gpiozero import Device
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
from loguru import logger

Device.pin_factory = PiGPIOFactory()

s0 = AngularServo(18, min_pulse_width=0.5/1000,
                  max_pulse_width=2.5/1000, min_angle=-135, max_angle=135)
# s1 = AngularServo(18, min_pulse_width=0.5/1000,
#                   max_pulse_width=2.5/1000, min_angle=-135, max_angle=135)
# s2 = AngularServo(18, min_pulse_width=0.5/1000,
#                   max_pulse_width=2.5/1000, min_angle=-135, max_angle=135)
# s3 = AngularServo(18, min_pulse_width=0.5/1000,
#                   max_pulse_width=2.5/1000, min_angle=-135, max_angle=135)
# s4 = AngularServo(18, min_pulse_width=0.5/1000,
#                   max_pulse_width=2.5/1000, min_angle=-135, max_angle=135)
# s5 = AngularServo(18, min_pulse_width=0.5/1000,
#                   max_pulse_width=2.5/1000, min_angle=-135, max_angle=135)

logger.info(f"pin_factory {s0.pin_factory}")

