# imports
from OpenGL.GL import GL_CULL_FACE, GL_DEPTH_TEST, glColor3f, glEnable

from core import Player, Renderer, TextureAtlas, logger
from misc import Sky
import threading

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
        self.texture_manager.add_from_folder("assets/textures/block/")
        self.texture_manager.save("assets/textures/atlas.png")
        self.texid = self.texture_manager.generate()
        
        # OpenGL stuff
        glEnable(GL_DEPTH_TEST)  # Enable depth testing
        glEnable(GL_CULL_FACE)  # Enable culling
        
        # Add a block
        x, y, z = 0, 0, 0
        X, Y, Z = 1, 1, 1
        vertices = {
            "top": (x, Y, Z,  X, Y, Z,  X, Y, z,  x, Y, z, x, Y, Z, X, Y, z,),
            "bottom": (x, y, z,  X, y, z,  X, y, Z,  x, y, Z, x, y, z, X, y, Z,),
            "left": (x, y, z,  x, y, Z,  x, Y, Z,  x, Y, z, x, y, z, x, Y, Z,),
            "right": (X, y, Z,  X, y, z,  X, Y, z,  X, Y, Z, X, y, Z, X, Y, z,),
            "back": (x, y, Z,  X, y, Z,  X, Y, Z,  x, Y, Z, x, y, Z, X, Y, Z,),
            "front": (X, y, z,  x, y, z,  x, Y, z,  X, Y, z, X, y, z, x, Y, z,),
        }
        verts = []
        verts.extend(vertices["top"])
        verts.extend(vertices["bottom"])
        verts.extend(vertices["left"])
        verts.extend(vertices["right"])
        verts.extend(vertices["back"])
        verts.extend(vertices["front"])
        
        texCoords = []
        for i in range(6):
            texCoords.extend(self.texture_manager.texture_coords["grass_top.png"])
        self.verts, self.texCoords = verts, texCoords
        
    def drawcall(self):
        """
        Draw the world.
        """
        self.texture_manager.bind(self.texid)
        self.sky.drawcall()  # Draw the sky
        self.player.drawcall()  # Update the player
        self.renderer.drawcall()  # Draw the renderer
        
    def sharedcon(self):
        self.renderer.modify("default", self.verts, self.texCoords, 0)
