import pymurapi as mur
import cv2
from object_navigation import Navigation, FRONT, BOTTOM
from PID_controller import Controller
from moving import MovementManaging
from time import sleep
# import numpy as np

auv = mur.mur_init()
movement_managing = MovementManaging()
# CUBE_HEIGHT = 3.6
# RINGS_HEIGHTS = (1.6, 1.1, 1.9)

while movement_managing.get_queue_length():
    # auv.set_motor_power(4, 0)
    # auv.set_motor_power(0, 100)
    # auv.set_motor_power(1, 100)
    # cv2.imshow('Yellow', detect_color_center(auv.get_image_front(), (20, 50, 50), (35, 255, 255), (0, 0, 255)))
    delta_time = 0

    navigation_front = Navigation(auv.get_image_front(), FRONT)
    navigation_bottom = Navigation(auv.get_image_bottom(), BOTTOM)

    yellow_cnts = navigation_front.detect_color((20, 50, 50), (35, 255, 255))
    # black_cnts = navigation_bottom.detect_color((0, 0, 0), (0, 0, 30))

    fish_center = navigation_front.get_center(yellow_cnts)
    # cube_center = navigation_bottom.get_center(black_cnts)

    '''movement_managing.append_task()

    if fish_center:
        coords_stable(*fish_center, FRONT)'''

    navigation_front.get_image('Front')
    navigation_bottom.get_image('Bottom')

    cv2.waitKey(5)