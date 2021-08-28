import math
import serial
import time


# port_nano = serial.Serial(port="/dev/ttyAMA1", baudrate=115200)
port_arm = serial.Serial(port="/dev/ttyAMA2", baudrate=115200)
port_front_left = serial.Serial(port="/dev/ttyAMA1", baudrate=115200)
port_front_right = serial.Serial(port="/dev/ttyAMA3", baudrate=115200)
port_back_left = serial.Serial(port="/dev/ttyAMA4", baudrate=115200)
port_back_right = serial.Serial(port="/dev/ttyAMA0", baudrate=115200)


def get_size(a, b):
    """
    Calculate basic size parameters of the car
    Input a is the distance between the centers of two wheels in a row in cm
    Input b is the distance between the centers of two wheels in a column in cm
    For our car, a = 20.5cm and b = 21.2cm
    """
    c = a / 2 + b / 2
    return c


_size = get_size(20.5, 21.2)


def get_mess(L, S):
    """
    Generate the corresponding UART message
    L is the position
    S is the speed
    """
    m3 = int((L >> 24) & 0xff)  # Position
    m2 = int((L >> 16) & 0xff)
    m1 = int((L >> 8) & 0xff)
    m0 = int(L & 0xff)
    s1 = int((S >> 8) & 0xff)
    s0 = int(S & 0xff)
    VALUE = [0xAA, 0x59, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
             0xFF, 0xAA, 0x70, m3, m2, m1, m0, s1, s0, 0xFF, 0xFF]
    return VALUE


def get_pwm(L):
    """
    Generate the corresponding UART message
    i is the ID of the motor
    L is the speed1
    """

    m1 = int((L >> 8) & 0xff)  # velocity
    m0 = int(L & 0xff)
    VALUE = [0xAA, 0x4E, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
             0xFF, 0xAA, 0x0C, m1, m0, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    return VALUE

# Reset all the wheels (brake instantly)


def reset():
    VALUE = [0xAA, 0x4D, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    port_back_left.write(bytearray(VALUE))
    port_back_right.write(bytearray(VALUE))
    port_front_left.write(bytearray(VALUE))
    port_front_right.write(bytearray(VALUE))
    return 0


def pwm_move(angle, speed):
    """
    PWM open-loop moving
    Size is the c returned by calSize function
    Angle is the motion direction angle in radian, 0 at forward direction (posotive y-axis), positive for counter-clockwise
    Speed is the PWM-controlled speed (open-loop), between -4700 and 4700
    """
    if (speed > 4700) | (speed < -4700):
        print('Error! Speed is too large.')
        return 0

    Sx = speed * math.cos(angle + math.pi/2)
    Sy = speed * math.sin(angle + math.pi/2)

    # Calculate the position of each motor
    S1 = round(Sy - Sx)  # 0.5 is for rounding
    S2 = round(Sy + Sx)
    S3 = round(Sy - Sx)
    # The minus sign for motor 1 and 4 is due to their installation direction
    S4 = round(Sy + Sx)

    # Generate the UART messages
    VALUE1 = get_pwm(S1)
    VALUE2 = get_pwm(S2)
    VALUE3 = get_pwm(S3)
    VALUE4 = get_pwm(S4)

    # Send messages
    port_front_right.write(bytearray(VALUE1))
    port_front_left.write(bytearray(VALUE2))
    port_back_left.write(bytearray(VALUE3))
    port_back_right.write(bytearray(VALUE4))
    print(bytearray(VALUE1))
    print(bytearray(VALUE2))
    print(bytearray(VALUE3))
    print(bytearray(VALUE4))


def pid_move(angle, distance, speed, orientation):
    """
    Motion control function
    1. angle is the motion direction angle in radian, 0 at forward direction (posotive y-axis), positive for counter-clockwise
    2. distance is the absolute length for moving. If distance == 0, the car rotates in z-axis
    3. orientation is the angle of the head of the car in radian, same direction with angle
    4. speed must share the same sign with distance
    """
    dis = distance * 135 / 25  # Convert the distance into cycles
    spd = speed * 32767 / 100

    if (dis > 2 ** 31) | (dis < -2 ** 31):
        print('Error! Distance is too large.')
        return 0

    if (spd > 32767) | (spd < -32767):
        print('Error! Speed is too large.')
        return 0

    Lx = dis * math.cos(angle + math.pi/2)
    Ly = dis * math.sin(angle + math.pi/2)
    Sx = spd * math.cos(angle + math.pi/2)
    Sy = spd * math.sin(angle + math.pi/2)

    # Calculate the position of each motor
    L1 = int(Ly - Lx + orientation * _size + 0.5)  # 0.5 is for rounding
    L2 = int(Ly + Lx - orientation * _size + 0.5)
    L3 = int(Ly - Lx - orientation * _size + 0.5)
    L4 = int(Ly + Lx + orientation * _size + 0.5)
    S1 = int(Sy - Sx + orientation * _size + 0.5)  # 0.5 is for rounding
    S2 = int(Sy + Sx - orientation * _size + 0.5)
    S3 = int(Sy - Sx - orientation * _size + 0.5)
    S4 = int(Sy + Sx + orientation * _size + 0.5)

    # Generate the UART messages
    VALUE1 = get_mess(L1, S1)
    VALUE2 = get_mess(L2, S2)
    VALUE3 = get_mess(L3, S3)
    VALUE4 = get_mess(L4, S4)

    # Send messages
    port_front_right.write(bytearray(VALUE1))
    port_front_left.write(bytearray(VALUE2))
    port_back_left.write(bytearray(VALUE3))
    port_back_right.write(bytearray(VALUE4))


def dance():
    # pwm_move(0, 2000)
    pid_move(0, 500, 100, 0)
    time.sleep(1)
    reset()
    # time.sleep(1)
    # reset()
    # pid_move(math.pi/2, 100, 0)
    # time.sleep(1)
    # reset()
    # pid_move(-math.pi/2, 100, 0)
    # time.sleep(1)
    # reset()


if __name__ == "__main__":
    dance()
