'''навигация с помощью компьютерного зрения'''

import cv2

FRONT, BOTTOM = 0, 1


class Navigation:
    def __init__(self, image, camera_view):
        self.image = image
        self.camera_view = camera_view

    def get_camera_view(self):
        return self.camera_view

    def get_image(self, window_name):
        cv2.imshow(window_name, self.image)

    # объекты в заданном цветовом диапазоне
    def detect_color(self, lower_color, upper_color):
        img_hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img_hsv, lower_color, upper_color)
        # cv2.imshow('Mask', mask)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cntr_image = input_image.copy()
        # cv2.drawContours(input_image, contours, -1, center_color, 2)
        return contours

    # центр объекта
    def get_center(self, contours, center_color=(101, 107, 110)):
        for cnt in contours:
            if abs(cv2.contourArea(cnt)) > 150:
                moments = cv2.moments(cnt)
                try:
                    x, y = moments['m10'] / moments['m00'], moments['m01'] / moments['m00']
                    cv2.circle(self.image, (int(x), int(y)), 3, center_color)

                    return x, y
                except ZeroDivisionError:
                    return

    '''def get_center(self, contours, vertices_amount=0, center_color=(200, 21, 110)):
        for cnt in contours:
            if abs(cv2.contourArea(cnt)) > 150:
                hull = cv2.convexHull(cnt)
                approx = cv2.approxPolyDP(hull, cv2.arcLength(cnt, True) * 0.02, True)
                if len(approx) > vertices_amount:
                    # print(len(approx))
                    moments = cv2.moments(cnt)
                    x, y = moments['m10'] / moments['m00'], moments['m01'] / moments['m00']
                    cv2.circle(self.image, (int(x), int(y)), 3, center_color)

                    return x, y'''