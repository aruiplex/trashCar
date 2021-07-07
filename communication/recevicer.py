import io
import config.init
import json

from loguru import logger

_ted = config.init._init_ted()


def readline():
    null_line_number = 0
    f = io.open("./position.py", "r")
    while True:
        line = f.readline()
        yield line

        if line == "":
            null_line_number += 1

        if null_line_number == 5:
            raise EOFError


def vaildate(line):
    null_line_number = 0
    if line == "":
        null_line_number += 1
    if null_line_number == 5:
        raise Exception("end of trash car")


def serve():
    """
    serial port server
    """
    try:
        while True:
            msg_raw = _ted.readline()
            vaildate(msg_raw)
            msg = json.loads(msg_raw)
            yield msg
    except Exception as e:
        logger.warning(e)


if __name__ == "__main__":
    reader = readline()
    # while True:
    try:
        for i in range(0, 100):
            print(next(reader))
    except EOFError:
        print("//EOF")
        # print(next(reader))
