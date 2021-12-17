# imports
import pyglet
from pyglet.window import Window
from pyglet.gl import *

# inbuilt imports
import Classes as pycraft
from logger import *
from pyglet.window import key

class PyCraftWindow(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, caption = 'PyCraft')
        info('Window', 'Initializing PyCraftWindow...')

        self.model = pycraft.World(self)
        self.player = pycraft.Player(self)

        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)

        # initialize opengl
        # Background color
        glClearColor(0.5, 0.7, 1, 1)
        # Enable depth test
        glEnable(GL_DEPTH_TEST)
        # Enable backface culling
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)

        self.fps_display = pyglet.window.FPSDisplay(window=self)

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
        
    def on_draw(self):
        self.clear()
        self._setup_3d()
        self.player._translate()
        self.model.draw()
        self.fps_display.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        if self.lock:
            self.player.mouse_motion(dx, dy)

    def update(self, dt):
        self.model.update()
        self.player.update(self.keys)

    def on_close(self):
        pyglet.app.exit()

    def _setup_3d(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(70, self.width/self.height, 0.05, 1000)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
