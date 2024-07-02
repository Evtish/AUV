from PID_controller import Controller
from moving import MovementManaging
from object_navigation import FRONT, BOTTOM

IMAGE_H, IMAGE_W = 240, 320


class Stable:
    auv_x, auv_y = IMAGE_W // 2, IMAGE_H // 2
    target_x, target_y = 0, 0

    def set_coords(self, coords):
        self.target_x, self.target_y = coords

    def is_stable(self):
        return ((self.target_x - self.auv_x) ** 2 + (self.target_y - self.auv_y) ** 2) ** 0.5 < 2.0

    def coords_stable(self, camera):
        try:
            auv_x, auv_y = IMAGE_W // 2, IMAGE_H // 2
            error_x, error_y = self.target_x - auv_x, self.target_y - auv_y
            output_x, output_y = self.coords_stable.pid.computing(error_x), self.coords_stable.pid.computing(error_y)
            self.coords_stable.move_managing.set_side_speed(output_x)

            if camera == FRONT:
                self.coords_stable.move_managing.set_height_speed(output_y)

            elif camera == BOTTOM:
                self.coords_stable.move_managing.set_forward_speed(output_y)
        except AttributeError:
            self.coords_stable.pid = Controller(0.8, 0.3, 0.5)
            self.coords_stable.move_managing = MovementManaging()
