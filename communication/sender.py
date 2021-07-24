import json
from time import sleep
import config.init
from loguru import logger

_port = config.init._init_ted()


class Sender:
    def __init__(self) -> None:
        logger.info("sender init")

    def send(self, data: str):
        counter = 0

        while True:
            _port.write(str(data))
            response = _port.readline()

            if response == b"200 OK":
                logger.trace(f"{data} has send successfully")
                break

            sleep(0.02)

            if counter >= 5:
                logger.error(f"One communication is not send!\n{data}")
                break


class SenderStub:
    def __init__(self) -> None:
        logger.info("sender init")

    def send(self, data: str):
        logger.success(f"data: {data}, has been sent.")
