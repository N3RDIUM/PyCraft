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
        # Minimum size
        self.set_minimum_size(800, 500)

        # Key state handler
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)

        # Player
        self.player = Player((0, 100, 0), (0, 0), self)
        # Model
        self.model = World(self, self.player)
        pyglet.clock.schedule_interval(self.model.update, 1/60)

        # If the window is alive
        self.alive = True

    def push(self, pos, rot):
        """
        push

        * pushes the camera to the player

        :pos: the position of the player
        :rot: the rotation of the player
        """
        # Rotation and position
        rot = self.player.rot
        pos = self.player.pos
        # Push and rotate the camera
        glRotatef(-rot[0], 1, 0, 0)
        glRotatef(-rot[1], 0, 1, 0)
        glTranslatef(-pos[0], -pos[1], -pos[2])

    def on_close(self):
        """
        on_close

        * called when the window is closed
        """
        # Set alive to false
        self.alive = False

    @staticmethod
    def Projection():
        """
        Projection

        * sets the projection
        """
        # Set the projection and load identity
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

    @staticmethod
    def Model():
        """
        Model

        * sets the model
        """
        # Set the model and load identity
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set2d(self):
        """
        set2d
        
        * sets the projection to 2d
        """
        # Set perspective
        self.Projection()
        gluPerspective(0, self.width, 0, self.height)
        self.Model()

    def set3d(self):
        """
        set3d

        * sets the projection to 3d
        """
        # Set 3d perspective
        self.Projection()
        gluPerspective(70, self.width/self.height, 0.05, 1000)
        self.Model()

    def setLock(self, state):
        """
        setLock

        * sets the mouse lock

        :state: the state of the mouse lock
        """
        # Set the mouse lock
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
            # Inform the player of the mouse movement
            self.player.mouse_motion(dx, dy)

    def on_key_press(self, KEY, _MOD):
        """
        on_key_press

        * handles key presses

        :KEY: the key pressed
        :_MOD: the modifier
        """
        if KEY == key.ESCAPE:
            # Don't close the window
            pass
        elif KEY == key.E:
            # Toggle mouse lock
            self.mouse_lock = not self.mouse_lock

    @staticmethod
    def on_close():
        """
        on_close

        * called when the window is closed
        """
        # Close the window
        pyglet.app.exit()

    def update(self, dt):
        """
        update

        * updates the window
        """
        # Update the player
        self.player.update(dt, self.keys)

    def on_mouse_press(self, *args, **kwargs):
        """
        on_mouse_press

        * handles mouse presses
        """
        # Inform the player of the mouse click
        self.player.mouse_click = True

    def on_mouse_release(self, *args, **kwargs):
        """
        on_mouse_release
            
        * handles mouse releases
        """
        # Inform the player of the mouse release
        self.player.mouse_click = False

    def on_draw(self):
        """
        on_draw

        * draws the window
        """
        # Clear the screen
        self.clear()
        # Set the projection to 3d
        self.set3d()
        # Push the camera and draw the world
        self.push(self.player.pos, self.player.rot)
        self.model.draw()
