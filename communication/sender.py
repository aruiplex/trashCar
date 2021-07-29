import json
import socket
import time
from loguru import logger
from config.init import cfg

pi_ip = cfg["network"]["pi"]


class Sender():
    def __init__(self) -> None:
        logger.success("sender created.")

    def send(self, data: json):
        """Send the json format data

        Args:
            data (json): the date need to send 
        """
        ok = False
        while not ok:
            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.connect((pi_ip, 7021))
                raw = json.dumps(data).encode()
                self.s.sendall(raw)
                ok = True
            except:
                time.sleep(0.2)
    # def send_stub(self, data: json):
    #     raw = json.dumps(data).encode()
    #     logger.success(raw)

# def test():
# s = Sender()
# s.send({"clz": "cup", "phi": -0.09657364535103545, "coordinate": [-0.02523331561960583, 0.2604729354281893]})
