import pymurapi as mur

from time import time

auv = mur.mur_init()


class MovementManaging:
    yaw, depth = 0.0, 0.0
    height_speed, forward_speed, side_speed = 0.0, 0.0, 0.0
    delta_time = 0
    tasks_queue = []

    def set_yaw(self, val):
        self.yaw = val

    def set_depth(self, val):
        self.depth = val

    def set_height_speed(self, val):
        self.height_speed = limit(val, -100, 100)

    def set_forward_speed(self, val):
        self.forward_speed = limit(val, -100, 100)

    def set_side_speed(self, val):
        self.side_speed = limit(val, -100, 100)

    def append_task(self, action):
        self.tasks_queue.append(action)

    def pop_task(self):
        return self.tasks_queue.pop(0)

    def get_queue_length(self):
        return len(self.tasks_queue)

    def turn_off_motors(self):
        for i in range(5):
            auv.set_motor_power(i, 0)
        self.height_speed, self.forward_speed, self.side_speed = 0.0, 0.0, 0.0

    def update(self):
        cur_time = round(time() * 1000)
        if cur_time - self.delta_time > 15:
            self.delta_time = cur_time
            move(self.forward_speed, 0, 1)
            move(self.height_speed, 2, 3)
            move(self.side_speed, 4)
            rotate(self.forward_speed)


def limit(input_val, min_val, max_val):
    if input_val < min_val:
        return min_val
    elif input_val > max_val:
        return max_val
    return input_val


def move(speed, *motors):
    for motor in motors:
        auv.set_motor_power(motor, speed)


def rotate(speed):
    auv.set_motor_power(0, -speed)
    auv.set_motor_power(1, speed)


'''def set_depth(new_depth):
    try:
        error = auv.get_depth() - new_depth
        output = limit(set_depth.pid.computing(error), -100, 100)

        auv.set_motor_power(2, output)
        auv.set_motor_power(3, output)
    except AttributeError:
        set_depth.pid = Controller(80, 0, 50)'''


'''def set_rotate(new_angle):
    def convert_angle(angle):
        angle %= 360
        if angle > 180:
            return angle - 360
        elif angle < -180:
            return angle + 360
        return angle

    try:
        error = auv.get_yaw() - convert_angle(new_angle)
        output = limit(set_rotate.pid.computing(error), -100, 100)

        auv.set_motor_power(0, -output)
        auv.set_motor_power(1, output)
    except AttributeError:
        set_rotate.pid = Controller(0.8, 0.3, 0.5)'''