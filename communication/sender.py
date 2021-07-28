import json
from time import sleep
import socket


class Sender():
    def __init__(self) -> None:
        print("sender created.")

    def send(self, data):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("127.0.0.1", 7021))
        self.s.send(data)


s = Sender()
l = ["bottle", "paper", "orange", "battery", "cup"]
s.send(str(l).encode())
s.send(b"bye")
