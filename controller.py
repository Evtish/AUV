'''ПИД-регулятор'''

import pymurapi as mur
from time import time

auv = mur.mur_init()


class Controller:
    prev_time, prev_error = 0, 0
    integral = 0

    def __init__(self, kP=0.8, kI=0.3, kD=0.5):
        self.kP = kP
        self.kI = kI
        self.kD = kD

    def computing(self, error):
        delta_time = time() - self.prev_time
        self.integral += self.kI * error * delta_time
        derivative = self.kD * (error - self.prev_error) / delta_time

        self.prev_time, self.prev_error = time(), error
        return self.kP * error + self.kI * self.integral + self.kD * derivative


def limit(input_val, min_val, max_val):
    if input_val < min_val:
        return min_val
    elif input_val > max_val:
        return max_val


def set_depth(new_depth):
    try:
        error = auv.get_depth() - new_depth
        output = limit(set_depth.pid.computing(error), -100, 100)

        auv.set_motor_power(3, output)
        auv.set_motor_power(4, output)
    except AttributeError:
        set_depth.pid = Controller(70, 20, 5)


def set_moving(speed, new_angle):
    def convert_angle(angle):
        angle %= 360
        if angle > 180:
            return angle - 360
        elif angle < -180:
            return angle + 360
        return angle

    try:
        error = auv.get_yaw() - convert_angle(new_angle)
        output = set_depth.pid.computing(error)

        auv.set_motor_power(0, limit(speed - output, -100, 100))
        auv.set_motor_power(1, limit(speed + output, -100, 100))
    except AttributeError:
        set_depth.pid = Controller()