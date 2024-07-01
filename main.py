import pymurapi as mur
import cv2
from navigation import Navigation
from controller import set_moving, set_depth
# import numpy as np

auv = mur.mur_init()
# IMAGE_H, IMAGE_W = 240, 320
# CUBE_HEIGHT = 3.6
# RINGS_HEIGHTS = (1.6, 1.1, 1.9)

while True:
    # auv.set_motor_power(0, 100)
    # auv.set_motor_power(1, 100)
    # cv2.imshow('Yellow', detect_color_center(auv.get_image_front(), (20, 50, 50), (35, 255, 255), (0, 0, 255)))
    navigation_front = Navigation(auv.get_image_front())
    navigation_bottom = Navigation(auv.get_image_bottom())

    yellow_cnts = navigation_front.detect_color((20, 50, 50), (35, 255, 255))
    black_cnts = navigation_bottom.detect_color((0, 0, 0), (0, 0, 30))

    fish_center = navigation_front.get_center(yellow_cnts)
    cube_center = navigation_bottom.get_center(black_cnts)

    navigation_front.get_image('Front')
    navigation_bottom.get_image('Bottom')

    '''print('fish:')
    if fish_center and len(fish_center) == 2:
        print(*fish_center)
    else:
        print('none')

    print('cube:')
    if cube_center and len(cube_center) == 2:
        print(*cube_center)
    else:
        print('none')'''

    cv2.waitKey(5)