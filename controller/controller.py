from communication.recevicer import Listener
from loguru import logger
from config.init import cfg
from movement.move import move_gap


def serve():
    l = Listener()
    curr_position = 0
    counter = 0
    while True:
        # 目前的类别
        clz = l.recevice()
        logger.success(f"clz: {clz}")
        # 车身要移动的位置
        next_gap = cfg["items"][str(clz)]
        gap = curr_position - next_gap
        # 移动
        move_gap[gap]()
        counter += 1
        curr_position = next_gap
        if counter == 5:
            # kick()
            logger.success("now kick")
            break

    logger.success("now all program finish")
