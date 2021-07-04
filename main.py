from sense.detect import main_cv
import config.init
from loguru import logger

# global configuration
cfg = config.init.read_cfg()


def main():
    main_cv(cfg["cv"])


if __name__ == "__main__":
    main()
