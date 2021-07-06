from pathlib import Path
import sys
from sense.detect import main_cv
import config.init
from loguru import logger

# global configuration
cfg = config.init.read_cfg()

# todo:
# FILE = Path(__file__).absolute()
# sys.path.append(FILE.parents[0].as_posix())  # add yolov5/ to path


def main():
    logger.level("DEBUG")
    # use json directly pass the arguments
    main_cv(cfg["cv"])


if __name__ == "__main__":
    main()
