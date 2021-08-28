import io
# json 5 can support comments
import json5
from loguru import logger


def _read_cfg() -> dict:
    """load config file for globle

    Returns:
        dict: configuration
    """
    with io.open("./cfg.json5") as f:
        logger.info("config load")
        return json5.load(f, encoding="utf-8")


# global configuration
cfg = _read_cfg()
