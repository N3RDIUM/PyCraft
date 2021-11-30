# imports
import pyglet
from pyglet.gl import *
from pyglet.window import key
import time
from logger import *
logging.basicConfig(level=logging.INFO)

from Classes import *

# Window class
class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        """
        Window

        * the window class

        :args:
        :kwargs:
        """
        super().__init__(*args, **kwargs)
        info("Window", "Initializing window")
        self.set_minimum_size(800, 500)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)

        self.player = Player((0, 20, 0), (0, 0), self)
        self.model = World(self, self.player)
        pyglet.clock.schedule_interval(self.model.update, 1/60)

        self.alive = True

    def push(self, pos, rot):
        """
        push

        * pushes the camera to the player

        :pos: the position of the player
        :rot: the rotation of the player
        """
        rot = self.player.rot
        pos = self.player.pos
        glRotatef(-rot[0], 1, 0, 0)
        glRotatef(-rot[1], 0, 1, 0)
        glTranslatef(-pos[0], -pos[1], -pos[2])

    def on_close(self):
        """
        on_close

        * called when the window is closed
        """
        self.alive = False

    @staticmethod
    def Projection():
        """
        Projection

        * sets the projection
        """
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

    @staticmethod
    def Model():
        """
        Model

        * sets the model
        """
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set2d(self):
        """
        set2d
        
        * sets the projection to 2d
        """
        self.Projection()
        gluPerspective(0, self.width, 0, self.height)
        self.Model()

    def set3d(self):
        """
        set3d

        * sets the projection to 3d
        """
        self.Projection()
        gluPerspective(70, self.width/self.height, 0.05, 1000)
        self.Model()

    def setLock(self, state):
        """
        setLock

        * sets the mouse lock

        :state: the state of the mouse lock
        """
        self.lock = state
        self.set_exclusive_mouse(state)

    lock = False
    mouse_lock = property(lambda self: self.lock, setLock)

    def on_mouse_motion(self, x, y, dx, dy):
        """
        on_mouse_motion

        * handles mouse movement

        :x: the x position
        :y: the y position
        :dx: the change in x
        :dy: the change in y
        """
        if self.mouse_lock:
            self.player.mouse_motion(dx, dy)

    def on_key_press(self, KEY, _MOD):
        """
        on_key_press

        * handles key presses

        :KEY: the key pressed
        :_MOD: the modifier
        """
        if KEY == key.ESCAPE:
            pass
        elif KEY == key.E:
            self.mouse_lock = not self.mouse_lock

    @staticmethod
    def on_close():
        """
        on_close

        * called when the window is closed
        """
        pyglet.app.exit()

    def update(self, dt):
        """
        update

        * updates the window
        """
        self.player.update(dt, self.keys)

    def on_mouse_press(self, *args, **kwargs):
        """
        on_mouse_press

        * handles mouse presses
        """
        self.player.mouse_click = True

    def on_mouse_release(self, *args, **kwargs):
        """
        on_mouse_release
            
        * handles mouse releases
        """
        self.player.mouse_click = False

    def on_draw(self):
        """
        on_draw

        * draws the window
        """
        self.clear()
        self.set3d()
        self.push(self.player.pos, self.player.rot)
        self.model.draw()
