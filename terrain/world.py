# imports
from OpenGL.GL import GL_CULL_FACE, GL_DEPTH_TEST, glEnable

from core import Player, Renderer, TextureAtlas, logger
from core.pcdt import open_pcdt
from terrain.chunk import Chunk
from misc import Sky
import json
import importlib
import os

class World:
    """
    World

    The world class for PyCraft.
    """
    RENDER_DISTANCE = 1
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
        self.scheduled_chunks = []
        self.chunks = {}
        
        # OpenGL stuff
        glEnable(GL_DEPTH_TEST)  # Enable depth testing
        glEnable(GL_CULL_FACE)  # Enable culling
        
        # Generate the world
        self.generate()
        
    def generate_chunk(self, position):
        new = Chunk(self, position)
        new.generate()
        self.chunks[new.buffer_id] = new
        
    def generate(self):
        for x in range(-self.RENDER_DISTANCE, self.RENDER_DISTANCE + 1):
            for z in range(-self.RENDER_DISTANCE, self.RENDER_DISTANCE + 1):
                self.generate_chunk((x, 0, z))
        
    def drawcall(self):
        """
        Draw the world.
        """
        self.texture_manager.bind(self.texid)
        self.sky.drawcall()  # Draw the sky
        self.player.drawcall()  # Update the player
        self.renderer.drawcall()  # Draw the renderer
        
    def sharedcon(self):
        # Listen for pcdt files in cache/vbo_add
        files = os.listdir("cache/vbo_add")
        for file in files:
            try:
                data = json.loads(open_pcdt(f"cache/vbo_add/{file}"))
                self.renderer.modify(data['id'], data['vertices'], data['texCoords'], -1)
                os.remove(f"cache/vbo_add/{file}")
            except:
                continue