import json
import socket
from loguru import logger


class Sender():
    def __init__(self) -> None:
        logger.success("sender created.")

    def send(self, data: json):
        """Send the json format data

        Args:
            data (json): the date need to send 
        """
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("127.0.0.1", 7021))
        raw = json.dumps(data).encode()
        self.s.sendall(raw)

    def send_stub(self, data: json):
        raw = json.dumps(data).encode()
        logger.success(raw)


s = Sender()
s.send({"a": 1})
