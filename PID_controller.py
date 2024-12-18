'''ПИД-регулятор'''

from time import time


class Controller:
    prev_time, prev_error, prev_val = 0, 0, 0
    integral = 0

    def __init__(self, kP, kI, kD):
        self.kP = kP
        self.kI = kI
        self.kD = kD

    def computing(self, error):
        cur_time = int(round(time() * 1000))
        delta_time = cur_time - self.prev_time
        try:
            self.integral += error * delta_time
            derivative = (error - self.prev_error) / delta_time
            cur_val = self.kP * error + self.kI * self.integral + self.kD * derivative
            self.prev_time, self.prev_error, self.prev_val = cur_time, error, cur_val
            return cur_val
        except ZeroDivisionError:
            return self.prev_val
