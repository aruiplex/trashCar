import math
import serial


port_nano = serial.Serial(port="/dev/ttyAMA1", baudrate=115200)
port_arm = serial.Serial(port="/dev/ttyAMA2", baudrate=115200)
port_wheel = serial.Serial(port="/dev/ttyAMA3", baudrate=115200)


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


def get_mess(i, L):
    """
    Generate the corresponding UART message
    i is the ID of the motor
    L is the position
    """
    m3 = int((L >> 24) & 0xff)  # Position
    m2 = int((L >> 16) & 0xff)
    m1 = int((L >> 8) & 0xff)
    m0 = int(L & 0xff)
    i_fun = int((i << 4) | 0xB)  # ID information
    VALUE = [0x48, i_fun, m3, m2, m1, m0, 0xFF, 0xFF, 0xFF, 0xFF]
    return VALUE

# Reset all the wheels (brake instantly)


def reset():
    VALUE = [0x48, 0x05, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    port_wheel.write(bytearray(VALUE))
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

    Sx = speed * math.cos(angle + 3.141592653589/2)
    Sy = speed * math.sin(angle + 3.141592653589/2)

    # Calculate the position of each motor
    S1 = -int(Sy - Sx + 0.5)  # 0.5 is for rounding
    S2 = int(Sy + Sx + 0.5)
    S3 = int(Sy - Sx + 0.5)
    # The minus sign for motor 1 and 4 is due to their installation direction
    S4 = -int(Sy + Sx + 0.5)

    # Generate the UART messages
    VALUE1 = get_mess(1, S1)
    VALUE2 = get_mess(2, S2)
    VALUE3 = get_mess(3, S3)
    VALUE4 = get_mess(4, S4)

    # Send messages
    port_wheel.write(bytearray(VALUE1))
    port_wheel.write(bytearray(VALUE2))
    port_wheel.write(bytearray(VALUE3))
    port_wheel.write(bytearray(VALUE4))
    print(bytearray(VALUE1))
    print(bytearray(VALUE2))
    print(bytearray(VALUE3))
    print(bytearray(VALUE4))


def pid_move(angle, distance, orientation):
    """
    Motion control function
    1. angle is the motion direction angle in radian, 0 at forward direction (posotive y-axis), positive for counter-clockwise
    2. distance is the absolute length for moving. If distance == 0, the car rotates in z-axis
    3. orientation is the angle of the head of the car in radian, same direction with angle
    """
    dis = distance * 200 / 25  # Convert the distance into cycles

    if (dis > 2 ** 31) | (dis < -2 ** 31):
        print('Error! Distance is too large.')
        return 0

    Lx = dis * math.cos(angle + math.pi/2)
    Ly = dis * math.sin(angle + math.pi/2)

    # Calculate the position of each motor
    L1 = -int(Ly - Lx + orientation * _size + 0.5)  # 0.5 is for rounding
    L2 = int(Ly + Lx - orientation * _size + 0.5)
    L3 = int(Ly - Lx - orientation * _size + 0.5)
    # The minus sign for motor 1 and 4 is due to their installation direction
    L4 = -int(Ly + Lx + orientation * _size + 0.5)

    # Generate the UART messages
    VALUE1 = get_mess(1, L1)
    VALUE2 = get_mess(2, L2)
    VALUE3 = get_mess(3, L3)
    VALUE4 = get_mess(4, L4)

    # Send messages
    port_wheel.write(bytearray(VALUE1))
    port_wheel.write(bytearray(VALUE2))
    port_wheel.write(bytearray(VALUE3))
    port_wheel.write(bytearray(VALUE4))


def dance():
    pid_move(0, 500, 0)
    pid_move(0, -500, 0)
    pid_move(math.pi/2, 500, 0)
    pid_move(-math.pi/2, 500, 0)


if __name__ == "__main__":
    dance()
