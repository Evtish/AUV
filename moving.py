import pymurapi as mur
from PID_controller import Controller
# from navigation import Navigation
from time import time

auv = mur.mur_init()
IMAGE_H, IMAGE_W = 240, 320
FRONT, BOTTOM = 0, 1


class MovementManager:
    yaw, depth = 0.0, 0.0
    height_speed, forward_speed, side_speed = 0.0, 0.0, 0.0
    delta_time = 0
    tasks_queue = []

    def get_yaw(self):
        return self.yaw

    def get_depth(self):
        return self.depth

    def get_height_speed(self):
        return self.height_speed

    def get_forward_speed(self):
        return self.forward_speed

    def get_side_speed(self):
        return self.side_speed

    def set_yaw(self, val):
        self.yaw = val

    def set_depth(self, val):
        self.depth = val

    def set_height_speed(self, val):
        self.height_speed = val

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

    def update_speed(self, camera_view):
        cur_time = int(round(time() * 1000))
        if cur_time - self.delta_time > 15:
            self.delta_time = cur_time
            auv.set_motor_power(4, self.side_speed)
            keep_yaw(self.forward_speed, self.yaw)
            keep_depth(self.depth)
            '''if camera_view == FRONT:
                # keep_yaw(self.yaw, self.forward_speed)
                auv.set_motor_power(2, self.height_speed)
                auv.set_motor_power(3, self.height_speed)
            elif camera_view == BOTTOM:
                keep_depth(self.depth)
                auv.set_motor_power(0, self.forward_speed)
                auv.set_motor_power(1, self.forward_speed)'''


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

    try:
        error = auv.get_yaw() - convert_angle(new_angle)
        output = keep_yaw.pid.computing(error)

        auv.set_motor_power(0, limit(speed - output, -100, 100))
        auv.set_motor_power(1, limit(speed + output, -100, 100))
    except AttributeError:
        keep_yaw.pid = Controller(1, 0, 1)


def keep_depth(new_depth):
    try:
        error = auv.get_depth() - new_depth
        output = limit(keep_depth.pid.computing(error), -100, 100)

        auv.set_motor_power(2, output)
        auv.set_motor_power(3, output)
    except AttributeError:
        keep_depth.pid = Controller(70, 0, 50)


def stabilize(target_x, target_y, manager, camera_view):
    try:
        x_center, y_center = target_x - IMAGE_W / 2, target_y - IMAGE_H / 2

        length = (x_center ** 2 + y_center ** 2) ** 0.5
        if length < 2.0:
            return True

        side_speed = limit(stabilize.side_pid.computing(x_center), -100, 100)
        manager.set_side_speed(side_speed)
        forward_speed = limit(stabilize.forward_pid.computing(y_center), -100, 100)
        manager.set_forward_speed(forward_speed)
        '''if camera_view == FRONT:
            height_speed = limit(pid.computing(y_center), -100, 100)
            stabilize.manager.set_height_speed(height_speed)
        elif camera_view == BOTTOM:
            forward_speed = limit(pid.computing(y_center), -100, 100)
            stabilize.manager.set_forward_speed(forward_speed)'''

        '''auv.set_motor_power(0, forward_speed)
        auv.set_motor_power(1, forward_speed)
        auv.set_motor_power(2, side_speed)
        auv.set_motor_power(3, side_speed)'''

        return False

    except AttributeError:
        # stabilize.manager = MovementManager()
        stabilize.forward_pid = Controller(35, 0, 25)
        stabilize.side_pid = Controller(0.5, 0, 0.3)
