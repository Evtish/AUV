'''ПИД-регулятор'''

from time import time


class Controller:
    prev_time, prev_error = 0, 0
    integral = 0

    def __init__(self, kP, kI, kD):
        self.kP = kP
        self.kI = kI
        self.kD = kD

    def computing(self, error):
        cur_time = round(time() * 1000)
        delta_time = cur_time - self.prev_time
        self.integral += self.kI * error * delta_time
        derivative = self.kD * (error - self.prev_error) / delta_time

        self.prev_time, self.prev_error = cur_time, error
        return self.kP * error + self.kI * self.integral + self.kD * derivative