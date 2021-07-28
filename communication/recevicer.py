import io
import json
import socket

from loguru import logger


class Listener():

    def __init__(self):
        """listen on the port and pass the connect socket to the receiver
        """
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 7021
        self.s.bind(("", port))
        self.s.listen(6)
        print(f"Server is listening on 127.0.0.1:{port}")


    def __listen(self):
        connection, addr = self.s.accept()
        print(f"Connected by {addr}")
    
        data = connection.recv(1024)
        print(f"data: {data}")
        return data
    
    def recevice(self):
        while True:
            data = self.__listen()
            if data == b"bye":
                print("shutdown")
                break
            
            l = data.decode()
            


l = Listener()
l.recevice()
