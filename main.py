import sys
from sense.detect import main_cv
from config.init import cfg
from loguru import logger


# todo:
# FILE = Path(__file__).absolute()
# sys.path.append(FILE.parents[0].as_posix())  # add yolov5/ to path


def main():
    logger.level("DEBUG")
    # use json directly pass the arguments
    main_cv(cfg["cv"])


if __name__ == "__main__":
    main()
