from communication.recevicer import Listener
from loguru import logger
from config.init import cfg
from movement.move import perform_strech, move_gap, move, kick, perform_block_cancel, perform_block
import time
import math


def serve():
    l = Listener()
    curr_position = 0
    counter = 0
    # 离开出发区
    move(0, 0.3, 4000,0)
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

        # 进球!
        if counter == 5:
            time.sleep(3)
            perform_strech()
            time.sleep(3)

            # 遮挡
            # perform_block()
            time.sleep(2)
            # 前端补足距离
            # move(0, 0.7, 3000, 0)
            move(0, 0.72, 3000, 0)
            logger.success("move 0.7")
            time.sleep(3)
            logger.info(f"curr_position: {curr_position}")

            # bias
            kick_pre_dis = 0.35 - curr_position*0.07
            move(math.pi/2, kick_pre_dis, 4000)
            logger.success(f"move {kick_pre_dis}")
            time.sleep(2)
            logger.success("now kick")

            # 取消遮挡
            # perform_block()
            time.sleep(2)
            kick()

            break
        

    logger.success("now all program finish")
