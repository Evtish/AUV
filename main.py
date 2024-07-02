import pymurapi as mur
# import cv2
from object_navigation import Navigation, FRONT, BOTTOM
# from PID_controller import Controller
from moving import MovementManaging
from stable import Stable
from time import time
# import numpy as np

auv = mur.mur_init()
movement_managing = MovementManaging()
object_stable = Stable()
# CUBE_HEIGHT = 3.6
# RINGS_HEIGHTS = (1.6, 1.1, 1.9)
delta_time, navigation_front, navigation_bottom, yellow_cnts, fish_center = (None for _ in range(5))


def do_iteration():
    global delta_time, navigation_front, navigation_bottom, yellow_cnts, fish_center
    delta_time = 0

    navigation_front = Navigation(auv.get_image_front(), FRONT)
    navigation_bottom = Navigation(auv.get_image_bottom(), BOTTOM)

    yellow_cnts = navigation_front.detect_color((20, 50, 50), (35, 255, 255))
    # black_cnts = navigation_bottom.detect_color((0, 0, 0), (0, 0, 30))

    fish_center = navigation_front.get_center(yellow_cnts)
    # cube_center = navigation_bottom.get_center(black_cnts)

    navigation_front.get_image('Front')
    navigation_bottom.get_image('Bottom')


do_iteration()
if fish_center:
    object_stable.set_coords(fish_center)

movement_managing.append_task(object_stable.is_stable)

# while True:
cur_task = movement_managing.tasks_queue[0]
# do_iteration()

while fish_center and not cur_task():
    movement_managing.update_speed()
    do_iteration()
    object_stable.set_coords(fish_center)

movement_managing.stop_motors()