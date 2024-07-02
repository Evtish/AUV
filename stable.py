from PID_controller import Controller
from moving import MovementManaging
from object_navigation import FRONT, BOTTOM

pid = Controller(0.8, 0.3, 0.5)
move_managing = MovementManaging()
IMAGE_H, IMAGE_W = 240, 320


class Stable:
    auv_x, auv_y = IMAGE_W / 2, IMAGE_H / 2
    target_x, target_y = 0.0, 0.0

    def set_coords(self, coords):
        self.target_x, self.target_y = coords

    def is_stable(self):
        return ((self.target_x - self.auv_x) ** 2 + (self.target_y - self.auv_y) ** 2) ** 0.5 < 2.0

    def coords_stable(self, camera):
        auv_x, auv_y = IMAGE_W // 2, IMAGE_H // 2
        error_x, error_y = self.target_x - auv_x, self.target_y - auv_y
        output_x, output_y = pid.computing(error_x), pid.computing(error_y)
        move_managing.set_side_speed(output_x)
        print('side')

        if camera == FRONT:
            move_managing.set_height_speed(output_y)
            print('height')

        elif camera == BOTTOM:
            move_managing.set_forward_speed(output_y)
            print('forward')


'''if __name__ == '__main__':
    # stbl = Stable()
    # stbl.set_coords((100, 100))
    # while True:
    #     stbl.coords_stable(FRONT)
    auv_x, auv_y = IMAGE_W // 2, IMAGE_H // 2
    target_x, target_y = 100, 100
    error_x, error_y = target_x - auv_x, target_y - auv_y
    output_x, output_y = pid.computing(error_x), pid.computing(error_y)
    move_managing.set_side_speed(output_x)
    print(move_managing.side_speed)'''