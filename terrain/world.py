# imports
from OpenGL.GL import GL_CULL_FACE, GL_DEPTH_TEST, glEnable

from core import Player, Renderer, TextureAtlas, logger
from terrain.chunk import Chunk
from misc import Sky
import importlib

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
        self.texture_manager = TextureAtlas()
        self.renderer = Renderer(
            window=window, texture_manager=self.texture_manager)

        # Load the textures
        self.texture_manager.add_from_folder("assets/textures/block/", "_internals")
        self.texture_manager.save("assets/textures/atlas.png")
        self.texid = self.texture_manager.generate()
        
        # Load blocks
        self.blocks = importlib.import_module("terrain.block").blocks
        
        # Just create one chunk for now
        self.chunk = Chunk(self, (0, 0, 0))
        self.chunk.generate()
        
        # OpenGL stuff
        glEnable(GL_DEPTH_TEST)  # Enable depth testing
        glEnable(GL_CULL_FACE)  # Enable culling
        
    def drawcall(self):
        """
        Draw the world.
        """
        self.texture_manager.bind(self.texid)
        self.sky.drawcall()  # Draw the sky
        self.player.drawcall()  # Update the player
        self.renderer.drawcall()  # Draw the renderer
        
    def sharedcon(self):
        pass
