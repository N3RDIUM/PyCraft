# imports
from random import randint

from OpenGL.GL import GL_CULL_FACE, GL_DEPTH_TEST, glColor3f, glEnable

from core import Player, Renderer, TextureManager, logger
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
        self.texture_manager = TextureManager(1024)
        self.renderer = Renderer(window=window, texture_manager=self.texture_manager)
        
        # Load the textures
        self.texture_manager.add_from_folder("assets/textures/block")

        # Add random data to the renderer
        for i in range(100):
            self.renderer.modify("default", [randint(0, 10), randint(
                0, 10), randint(0, 10)], self.texture_manager.get_texture_coords("dirt.png"), i*3)

    def drawcall(self):
        """
        Draw the world.
        """
        glEnable(GL_DEPTH_TEST)  # Enable depth testing
        glEnable(GL_CULL_FACE)  # Enable culling

        self.sky.drawcall()  # Draw the sky
        self.player.drawcall()  # Update the player
        self.renderer.drawcall()  # Draw the renderer
