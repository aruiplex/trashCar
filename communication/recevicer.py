import config.init
import json

_ted = config.init._init_ted()


def serve():
    """
    serial port server
    """
    while True:
        msg_raw = _ted.readline()
        msg = json.loads(msg_raw)
        yield msg
