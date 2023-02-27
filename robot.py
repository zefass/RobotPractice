import cv2
import numpy as np
from PIL import ImageGrab
from ursina import *
import math

def analize():
    signal = 'no signal'
    screenshot = ImageGrab.grab()
    rgb = np.array(screenshot)
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([30, 70, 70])
    higher_blue = np.array([120, 255, 120])

    mask = cv2.inRange(hsv, lower_blue, higher_blue)

    M = cv2.moments(mask, 1)

    if M['m00'] != 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        cv2.circle(bgr, (cx, cy), 25, (0, 0, 225), -1)

        if cx < 800:
            cv2.putText(bgr, 'Turn left', (40, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
            signal = 'left'
        if cx > 1100:
            cv2.putText(bgr, 'Turn right', (40, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
            signal = 'right'
        if (cx > 800) & (cx < 1100):
            cv2.putText(bgr, 'Go forward', (40, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            signal = 'forward'

    cv2.line(bgr, (800, 0), (800, 1080), (0, 0, 255), 5)
    cv2.line(bgr, (1100, 0), (1100, 1080), (0, 0, 255), 5)

    cv2.imshow('Res', cv2.resize(bgr, (480, 270)))

    return signal
class Scene(Entity):
    def __init__(self):
        super().__init__()
        self.model = 'quad'
        self.texture = 'map'
        self.scale_x = 45
        self.scale_y = 45
        self.rotation_x = 90
        self.position = (0, 0, 0)


class Player(Entity):
    def __init__(self):
        super().__init__()
        camera.position = [-16.741268157958984, 4, -16.832792282104492]
        camera.rotation_x = 45
        camera.rotation_y = 361.1536560058594
        self.a = 4.732460266782609 #angle
        self.r = 0.025 #radius
        self.v = [1, 1] #velocity
        self.l = 0.5 #distance between wheels
        self.k = 30 #rotation coefficient
        self.s = 20 #speed
        self.pic = analize()

    def update(self):

        if self.pic == 'forward':
            camera.x += self.s * (self.r / 2) * (self.v[0] + self.v[1]) * math.cos(self.a)
            camera.z -= self.s * (self.r / 2) * (self.v[0] + self.v[1]) * math.sin(self.a)

        if self.pic == 'right':
            self.a += math.radians((self.r / self.l) * (self.k * self.v[1] - self.v[0]))
            camera.rotation_y += (self.r / self.l) * (self.k * self.v[1] - self.v[0])

        if self.pic == 'left':
            self.a += math.radians((self.r / self.l) * (self.v[1] - self.k * self.v[0]))
            camera.rotation_y += (self.r / self.l) * (self.v[1] - self.k * self.v[0])

        self.pic = analize()



app = Ursina()

bot = Player()
land = Scene()

app.run()