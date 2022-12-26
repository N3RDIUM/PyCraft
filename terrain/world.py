# imports
from random import randint

from OpenGL.GL import *  # Import OpenGL

from core import Player, Renderer, logger
from misc import Sky


class World:
    """
    World

    The world class for PyCraft.
    """

    def __init__(self, window=None):
        """
        Initialize the world.
        """
        logger.info("[World] Initializing world...")

        # Window properties
        self.window = window

        # Initialize
        self.sky = Sky()
        self.player = Player(window=window, world=self)
        self.renderer = Renderer(window=window)

    def _(self):
        # Add random data to the renderer
        for i in range(100):
            self.renderer.modify("default", [randint(0, 10), randint(0, 10), randint(0, 10)], [0.0, 0.0, 0.0], i*3)

    def drawcall(self):
        """
        Draw the world.
        """
        glEnable(GL_DEPTH_TEST)  # Enable depth testing
        glEnable(GL_CULL_FACE)  # Enable culling

        self.sky.drawcall()  # Draw the sky
        self.player.drawcall()  # Update the player
        glColor3f(0.0, 1.0, 0.0)  # Set the color to green
        self.renderer.drawcall() # Draw the renderer
        
        self._() # Add random data to the renderer
