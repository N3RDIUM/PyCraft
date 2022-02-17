# imports
import pyglet
from pyglet.window import Window
from pyglet.gl import *

# inbuilt imports
import Classes as pycraft
from logger import *
from pyglet.window import key

class PyCraftWindow(Window):
    """
    PyCraftWindow

    * The PyCraft Window
    """
    def __init__(self, shader, world_update_func, *args, **kwargs):
        """
        PyCraftWindow.__init__

        * Initializes the window
        """
        super().__init__(*args, **kwargs, caption = 'PyCraft')
        info('Window', 'Initializing PyCraftWindow...')

        self.model = pycraft.World(self)
        self.player = pycraft.Player(shader, self)

        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)

        self.fps_display = pyglet.window.FPSDisplay(window=self)
        self.world_update_func = world_update_func

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
        self.player._update_shader()
        self.clear()
        self._setup_3d()
        self.player._translate()
        self.model.draw()
        self.fps_display.label.text = self.fps_display.label.text + "     " + "Block: " + self.player.current_block_type if not "Block: " + self.player.current_block_type in self.fps_display.label.text else self.fps_display.label.text
        self.fps_display.label.color = (0, 0, 0, 200)
        self.fps_display.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        if self.lock:
            self.player.mouse_motion(dx, dy)

    def update(self, dt):
        self.model.update()
        self.player.update(self.keys)

    def on_mouse_press(self, button, modifiers, *args, **kwargs):
        if args[0] == 1:
            self.player.mouse_click = True
            pyglet.clock.schedule_once(self.release, 0.1)
        else:
            self.player.right_click = True
            pyglet.clock.schedule_once(self.release, 0.1)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.player.change_block(scroll_y)
    
    def release(self, dt):
        self.player.mouse_click = False
        self.player.right_click = False

    @staticmethod
    def on_close():
        pyglet.app.exit()

    def _setup_3d(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(70, self.width/self.height, 0.05, 1000)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
