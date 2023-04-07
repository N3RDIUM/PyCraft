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
        self.texture_manager = TextureManager()
        self.renderer = Renderer(
            window=window, texture_manager=self.texture_manager)

        # Load the textures
        self.texture_manager.load_textures("assets/textures/block")
        self.texture_manager.bind()  # Bind the texture manager

        # OpenGL stuff
        glEnable(GL_DEPTH_TEST)  # Enable depth testing
        glEnable(GL_CULL_FACE)  # Enable culling
        
        # Add a plane
        for x in range(-10, 10):
            for z in range(-10, 10):
                self.add_block((x, -1, z))
                self.add_block((x,  0, z))

    def add_block(self, position):
        x, y, z = position
        verts = [
            0, 1, 1,
            1, 1, 1,
            1, 1, 0,
            0, 1, 0,
            0, 1, 1,
            1, 1, 0,
            0, 0, 0,
            1, 0, 0,
            1, 0, 1,
            0, 0, 1,
            0, 0, 0,
            1, 0, 1,
            0, 0, 0,
            0, 0, 1,
            0, 1, 1,
            0, 1, 0,
            0, 0, 0,
            0, 1, 1,
            1, 0, 1,
            1, 0, 0,
            1, 1, 0,
            1, 1, 1,
            1, 0, 1,
            1, 1, 0,
            0, 0, 1,
            1, 0, 1,
            1, 1, 1,
            0, 1, 1,
            0, 0, 1,
            1, 1, 1,
            1, 0, 0,
            0, 0, 0,
            0, 1, 0,
            1, 1, 0,
            1, 0, 0,
            0, 1, 0
        ]
        for i in range(0, len(verts), 3):
            verts[i] += x
            verts[i + 1] += y
            verts[i + 2] += z
        self.renderer.modify("default", tuple(
            verts), self.texture_manager.get_texcoords("grass_top.png") * 6, -1)

    def drawcall(self):
        """
        Draw the world.
        """
        self.sky.drawcall()  # Draw the sky
        self.player.drawcall()  # Update the player
        self.texture_manager.bind()  # Bind the texture manager
        self.renderer.drawcall()  # Draw the renderer
