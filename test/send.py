import socket
from loguru import logger

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("127.0.0.1", 7021))
    data = "hello world"
    s.send(data.encode())
    logger.success(data)
