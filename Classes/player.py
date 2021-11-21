from pyglet.window import key
from pyglet.gl import *
import math

class Player:
    def __init__(self, pos=(0, 0, 0), rot=(0, 0), parent=None):
        self.pos = list(pos)
        self.rot = list(rot)
        self.x = 0
        self.y = 0
        self.z = 0
        self.rotY = 0
        self.rotX = 0
        self.parent = parent

        self.movable = {"left":True, "right":True, "forward":True, "backward":True, "up":True, "down":True}

    def mouse_motion(self, dx, dy):
        self.rot[0] += dy/8
        self.rot[1] -= dx/8
        if self.rot[0]>90:
            self.rot[0] = 90
        elif self.rot[0] < -90:
            self.rot[0] = -90
        
    def _collide(self):
        x_int = int(self.pos[0])
        y_int = int(self.pos[1])
        z_int = int(self.pos[2])

        if self.parent.model.block_exists((x_int, y_int-2, z_int)):
            print("Can\'t move down")
            self.movable["down"] = False
        if self.parent.model.block_exists((x_int, y_int+2, z_int)):
            print("Can\'t move up")
            self.movable["up"] = False
        if self.parent.model.block_exists((x_int-2, y_int, z_int)):
            print("Can\'t move left")
            self.movable["left"] = False
        if self.parent.model.block_exists((x_int+2, y_int, z_int)):
            print("Can\'t move right")
            self.movable["right"] = False
        if self.parent.model.block_exists((x_int, y_int, z_int-2)):
            print("Can\'t move backward")
            self.movable["backward"] = False
        if self.parent.model.block_exists((x_int, y_int, z_int+2)):
            print("Can\'t move forward")
            self.movable["forward"] = False

    def update(self,dt,keys):
        sens = 0.3
        s = dt*10
        rotY = -self.rot[1]/180*math.pi
        dx, dz = s*math.sin(rotY), math.cos(rotY)
        self._collide()
        if keys[key.W] and self.movable["forward"]:
            self.pos[0] += dx*sens
            self.pos[2] -= dz*sens
        if keys[key.S] and self.movable["backward"]:
            self.pos[0] -= dx*sens
            self.pos[2] += dz*sens
        if keys[key.A] and self.movable["left"]:
            self.pos[0] -= dz*sens
            self.pos[2] -= dx*sens
        if keys[key.D] and self.movable["right"]:
            self.pos[0] += dz*sens
            self.pos[2] += dx*sens
        if keys[key.SPACE] and self.movable["up"]:
            self.pos[1] += s
        if keys[key.LSHIFT] and self.movable["down"]:
            self.pos[1] -= s

        self.x = self.pos[0]
        self.y = self.pos[2]
        self.z = self.pos[1]

        self.rotY = self.rot[0]
        self.rotX = self.rot[1]
