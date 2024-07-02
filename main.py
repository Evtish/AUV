import pymurapi as mur
# import cv2
from navigation import Navigation
from moving import MovementManaging, stabilize
# from time import sleep
# import numpy as np

auv = mur.mur_init()
manager = MovementManaging()
navigation_front = Navigation()
# navigation_bottom = Navigation()

# CUBE_HEIGHT = 3.6
# RINGS_HEIGHTS = (1.6, 1.1, 1.9)
# yellow_cnts, fish_center = None, None


'''def update_data():
    global yellow_cnts, fish_center
    navigation_front.set_image(auv.get_image_front())
    # navigation_bottom.set_image(auv.get_image_bottom())

    yellow_cnts = navigation_front.detect_color((20, 50, 50), (35, 255, 255))
    # black_cnts = navigation_bottom.detect_color((0, 0, 0), (0, 0, 30))

    fish_center = navigation_front.get_center(yellow_cnts)
    # cube_center = navigation_bottom.get_center(black_cnts)

    # navigation_front.get_image('Front')
    # navigation_bottom.get_image('Bottom')'''


def find_target():
    navigation_front.set_image(auv.get_image_front())
    yellow_cnts = navigation_front.detect_color((20, 50, 50), (35, 255, 255))
    return bool(navigation_front.get_center(yellow_cnts))


def stab_target():
    navigation_front.set_image(auv.get_image_front())
    yellow_cnts = navigation_front.detect_color((20, 50, 50), (35, 255, 255))
    fish_center = navigation_front.get_center(yellow_cnts)
    if stabilize(*fish_center):
        manager.stop_motors()
        return True
    return False


manager.set_yaw(0.0)
manager.set_depth(2.0)
manager.set_forward_speed(30)
manager.add_task(find_target)
manager.add_task(stab_target)

while True:
    # update_data()

    cur_task = manager.pop_task()
    while not cur_task():
        manager.update_speed()
        # update_data()

    if manager.get_queue_length() == 0:
        break