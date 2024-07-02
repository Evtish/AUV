import pymurapi as mur
from PID_controller import Controller

auv = mur.mur_init()


def limit(input_val, min_val, max_val):
    if input_val < min_val:
        return min_val
    elif input_val > max_val:
        return max_val
    return input_val


def set_depth(new_depth):
    try:
        error = auv.get_depth() - new_depth
        output = limit(set_depth.pid.computing(error), -100, 100)

        auv.set_motor_power(2, output)
        auv.set_motor_power(3, output)
    except AttributeError:
        set_depth.pid = Controller(80, 0, 50)


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
        set_depth.pid = Controller(0.8, 0.3, 0.5)