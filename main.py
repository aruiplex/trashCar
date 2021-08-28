from config.init import cfg
from loguru import logger
from controller.controller import serve
import movement.move 
import time
import math


if cfg["this"] == "nano":
    from sense.detect import main_cv

def _init_logger():
    logger.level("DEBUG")
    logger.add("./run/{time}.log", retention=5, catch=True)
    logger.bind(with_traceback=True).info("With traceback")


def main():
    _init_logger()
    if cfg["this"] == "nano":
        # use json directly pass the arguments
        main_cv(cfg["cv"])

    if cfg["this"] == "pi":
        movement.move.perform_init()
        logger.success("wait for enter to start")
        # 机械臂初始化
        # 正式开始程序
        while True:
            if input() == "":
                serve()
                logger.success("exit 0")
                exit(0)


        # serve()
        # logger.success("exit 0")
        # exit(0)


if __name__ == "__main__":
    main()

    # movement.move.move(0, 0.3, 4000, 0)
    # time.sleep(1.6)
    # movement.move.move(0,0.8,4000,0)
    # time.sleep(2)
    # movement.move.move(0,0.8,4000,0)
    # time.sleep(2)
    # movement.move.move(0,0.8,4000,0)
    # time.sleep(2)
    # movement.move.move(0,0.8,4000,0)
    # time.sleep(2)
    # movement.move.move(0,0.8,4000,0)
    # time.sleep(2)
    # movement.move.minus_3()
    # movement.move.plus_1()
    # time.sleep(3)
    # movement.move.plus_2()
    # time.sleep(3)
    # movement.move.minus_2()
    # time.sleep(3)
    # movement.move.plus_2()
    # time.sleep(3)
    # movement.move.minus_1()
    # time.sleep(3)
