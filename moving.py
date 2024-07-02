import pymurapi as mur
from PID_controller import Controller
from navigation import Navigation
from time import time

auv = mur.mur_init()
forward_pid = Controller(0.6, 0, 0.6)
IMAGE_H, IMAGE_W = 240, 320


class MovementManaging:
    yaw, depth = 0.0, 0.0
    forward_speed, side_speed = 0.0, 0.0
    delta_time = 0
    tasks_queue = []

    def get_yaw(self):
        return self.yaw

    def get_depth(self):
        return self.depth

    def get_forward_speed(self):
        return self.forward_speed

    def get_side_speed(self):
        return self.side_speed

    def set_yaw(self, val):
        self.yaw = val

    def set_depth(self, val):
        self.depth = val

    def set_forward_speed(self, val):
        self.forward_speed = val

    def set_side_speed(self, val):
        self.side_speed = val

    def add_task(self, task):
        self.tasks_queue.append(task)

    def pop_task(self):
        return self.tasks_queue.pop(0)

    def get_queue_length(self):
        return len(self.tasks_queue)

    def stop_motors(self):
        for i in range(5):
            auv.set_motor_power(i, 0)
        self.forward_speed, self.side_speed = 0.0, 0.0

    def update_speed(self):
        cur_time = int(round(time() * 1000))
        if cur_time - self.delta_time > 15:
            self.delta_time = cur_time
            keep_yaw(self.yaw, self.forward_speed)
            keep_depth(self.depth)
            auv.set_motor_power(2, self.side_speed)
            auv.set_motor_power(3, self.side_speed)


def limit(input_val, min_val, max_val):
    if input_val < min_val:
        return min_val
    elif input_val > max_val:
        return max_val
    return input_val


def keep_yaw(speed, new_angle):
    def convert_angle(angle):
        angle %= 360
        if angle > 180:
            return angle - 360
        elif angle < -180:
            return angle + 360
        return angle

    error = auv.get_yaw() - convert_angle(new_angle)
    output = forward_pid.computing(error)

    auv.set_motor_power(0, limit(speed - output, -100, 100))
    auv.set_motor_power(1, limit(speed + output, -100, 100))


def keep_depth(new_depth):
    try:
        error = auv.get_depth() - new_depth
        output = limit(keep_depth.pid.computing(error), -100, 100)

        auv.set_motor_power(2, output)
        auv.set_motor_power(3, output)
    except AttributeError:
        keep_depth.pid = Controller(70, 0, 50)


def stabilize(target_x, target_y):
    try:
        x_center, y_center = target_x - IMAGE_W / 2, target_y - IMAGE_H / 2

        length = (x_center ** 2 + y_center ** 2) ** 0.5
        if length < 2.0:
            return True

        forward_speed = limit(forward_pid.computing(y_center), -100, 100)
        side_speed = limit(stabilize.side_pid.computing(x_center), -100, 100)

        stabilize.managing.set_forward_speed(forward_speed)
        stabilize.managing.set_side_speed(side_speed)
        '''auv.set_motor_power(0, forward_speed)
        auv.set_motor_power(1, forward_speed)
        auv.set_motor_power(2, side_speed)
        auv.set_motor_power(3, side_speed)'''

        return False

    except AttributeError:
        stabilize.managing = MovementManaging()
        stabilize.side_pid = Controller(0.6, 0, 0.6)