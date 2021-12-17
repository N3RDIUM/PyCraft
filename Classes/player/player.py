# imports
from pyglet.window import key
from pyglet.gl import *
import math

# inbuilt imports
from logger import *
import Classes as pycraft

# player class
class Player:
    def __init__(self, parent=None):
        """
        Player

        * the first person controller

        :pos: the position of the player
        :rot: the rotation of the player
        :parent: the parent of the player
        """
        self.pos = [0, 5, 0]
        self.rot = [0, 0, 0]
        self.vel = [0, 0]
        self.x = 0
        self.y = 0
        self.z = 0
        self.rotY = 0
        self.rotX = 0
        self.parent = parent
        self.speed = 0.3
        self.pointing_at = [[0,0,0], [0,0,0]]

        self.block_exists = {"left": False, "right": False,
                             "forward": False, "backward": False, "up": False, "down": False}
        self.suffocating = False
        self.falling = False
        self.velocity_y = 0
        self.gravity = 0.01
        self.hit_range = 8
        self.friction = 0.25

        self.terminal_velocity = 5

        self.mouse_click = False

    def mouse_motion(self, dx, dy):
        """
        mouse_motion

        * handles mouse movement

        :dx: the change in x
        :dy: the change in y
        """
        self.rot[0] += dy/8
        self.rot[1] -= dx/8
        if self.rot[0] > 90:
            self.rot[0] = 90
        elif self.rot[0] < -90:
            self.rot[0] = -90
        self.rot[0] = self.rot[0]
        self.rot[1] = self.rot[1]

    def update(self, keys):
        """
        update

        * updates the player

        :dt: the delta time
        :keys: the keys pressed
        """
        sens = self.speed
        rotY = math.radians(-self.rot[1])
        dx, dz = math.sin(rotY), math.cos(rotY)
        
        if self.velocity_y > self.terminal_velocity:
            self.velocity_y = self.terminal_velocity
        if self.velocity_y < -self.terminal_velocity:
            self.velocity_y = -self.terminal_velocity

        if keys[key.W]:
            self.vel[0] += dx*sens
            self.vel[1] -= dz*sens
        if keys[key.S]:
            self.vel[0] -= dx*sens
            self.vel[1] += dz*sens
        if keys[key.A]:
            self.vel[0] -= dz*sens
            self.vel[1] -= dx*sens
        if keys[key.D]:
            self.vel[0] += dz*sens
            self.vel[1] += dx*sens
        if keys[key.SPACE] and not self.falling:
            self.velocity_y += 0.1
        if keys[key.LSHIFT]:
            self.velocity_y -= 0.1
        if keys[key.LCTRL]:
            self.speed = 0.5
        else:
            self.speed = 0.3

        self.pos[1] += self.velocity_y
        self.pos[0] += self.vel[0]
        self.pos[2] += self.vel[1]

        self.vel[0] *= self.friction
        self.vel[1] *= self.friction
        self.velocity_y *= self.friction

    def _translate(self):
        glRotatef(-self.rot[0], 1, 0, 0)
        glRotatef(-self.rot[1], 0, 1, 0)
        glTranslatef(-self.pos[0], -self.pos[1], -self.pos[2])
