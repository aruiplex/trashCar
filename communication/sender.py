import json
import config.init
from loguru import logger

# aruix: stub
# _ted = config.init._init_ted()
stub = config.init.Stub()
_ted = stub._init_ted()


class Sender:
    def __init__(self) -> None:
        logger.info("sender init")

    def send(self, data: str):
        # aruix: stub
        # _ted.write(str(data))
        logger.info(f"<SEND> has send: {str(data).encode()}")
