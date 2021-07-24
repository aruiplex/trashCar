from sense.detect import main_cv
from config.init import cfg
from loguru import logger


def _init_logger():
    logger.level("DEBUG")
    logger.add("./run/{time}.log", retention=5, catch=True)
    logger.bind(with_traceback=True).info("With traceback")


def main():
    _init_logger()
    # use json directly pass the arguments
    main_cv(cfg["cv"])


if __name__ == "__main__":
    main()
