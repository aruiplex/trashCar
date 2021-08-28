import socket
from loguru import logger


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    port = 7021
    s.bind(("", port))
    s.listen(6)
    logger.success(f"Server is listening on 127.0.0.1:{port}")
    while True:
        connection, addr = s.accept()
        with connection:
            logger.info(f"Connected by {addr}")
            data = bytearray([])
            while True:
                r = connection.recv(1)
                data += r
                if not r:
                    break
                    # continue

            logger.info(f"data: {data.decode()}")
