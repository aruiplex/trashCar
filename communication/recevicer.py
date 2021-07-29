import socket
from loguru import logger
import json

message_queue = []


def most_common(lst):
    # return max(set(lst), key=lst.count)
    clzs = []
    for item in lst:
        clzs.append(item["clz"])
    return max(set(clzs), key=clzs.count)


class Listener():
    def __init__(self):
        """listen on the port and pass the connect socket to the receiver
        """
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 7021
        self.s.bind(("", port))
        self.s.listen(6)
        logger.success(f"Server is listening on 127.0.0.1:{port}")

    def __listen(self)-> str:
        connection, addr = self.s.accept()
        with connection:
            logger.info(f"Connected by {addr}")
            data = bytearray()
            while True:
                r = connection.recv(1024)
                if not r:
                    break
                data += r
            return data.decode()

    def recevice(self):
        while True:
            raw = self.__listen()
            logger.info(f"data: {raw}")
            if raw == "bye":
                logger.success("shutdown")
                break
            if not raw:
                continue
            data = json.loads(raw)
            logger.info(data)
            message_queue.append(data)
            # if len(message_queue) >= 8:
            #     obj =  most_common(message_queue)
            #     message_queue.


l = Listener()
l.recevice()
