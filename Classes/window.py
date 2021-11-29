import pyglet
from pyglet.gl import *
from pyglet.window import key
import time
from logger import *

from Classes.player import *
from Classes.chunk import *
from Classes.world import *


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        log("Window", "Initializing window")
        self.set_minimum_size(800, 500)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)

        self.player = Player((0, 20, 0), (0, 0), self)
        self.model = World(self, self.player)
        pyglet.clock.schedule_interval(self.model.update, 1/60)

        self.alive = True

    def push(self, pos, rot):
        rot = self.player.rot
        pos = self.player.pos
        glRotatef(-rot[0], 1, 0, 0)
        glRotatef(-rot[1], 0, 1, 0)
        glTranslatef(-pos[0], -pos[1], -pos[2])

    def on_close(self):
        self.alive = False

    @staticmethod
    def Projection():
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

    @staticmethod
    def Model():
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set2d(self):
        self.Projection()
        gluPerspective(0, self.width, 0, self.height)
        self.Model()

    def set3d(self):
        self.Projection()
        gluPerspective(70, self.width/self.height, 0.05, 1000)
        self.Model()

    def setLock(self, state):
        self.lock = state
        self.set_exclusive_mouse(state)

    lock = False
    mouse_lock = property(lambda self: self.lock, setLock)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_lock:
            self.player.mouse_motion(dx, dy)

    def on_key_press(self, KEY, _MOD):
        if KEY == key.ESCAPE:
            pass
        elif KEY == key.E:
            self.mouse_lock = not self.mouse_lock

    @staticmethod
    def on_close():
        pyglet.app.exit()

    def update(self, dt):
        self.player.update(dt, self.keys)

    def on_mouse_press(self, *args, **kwargs):
        self.player.mouse_click = True

    def on_mouse_release(self, *args, **kwargs):
        self.player.mouse_click = False

    def on_draw(self):
        self.clear()
        self.set3d()
        self.push(self.player.pos, self.player.rot)
        self.model.draw()
