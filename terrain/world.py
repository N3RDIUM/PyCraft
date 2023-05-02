# imports
from OpenGL.GL import *

from core import Player, Renderer, TextureAtlas, logger
from core.pcdt import open_pcdt
from terrain.chunk import Chunk
from misc import Sky
from core.utils import position_to_string, string_to_position
import json
import time
import importlib
import os
import math

class World:
    """
    World

    The world class for PyCraft.
    """
    RENDER_DISTANCE = 2
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
        glEnable(GL_FOG)
        glFogi(GL_FOG_MODE, GL_LINEAR)
        glFogf(GL_FOG_DENSITY, 0.1)
        glFogf(GL_FOG_START, 0.0)
        glFogf(GL_FOG_END, self.RENDER_DISTANCE * Chunk.SIZE[0] / 3 * 2)
        glFogfv(GL_FOG_COLOR, self.sky.color)
        glHint(GL_FOG_HINT, GL_DONT_CARE)
        
        # Generate the world
        self.n = 0
        self.generate()
        self.to_generate = []
        
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
        self.n += 1
        time.sleep(1/60)
        # Listen for pcdt files in cache/vbo_add
        files = os.listdir("cache/vbo_add")
        for file in files:
            try:
                data = json.loads(open_pcdt(f"cache/vbo_add/{file}"))
                self.renderer.modify(data['id'], data['vertices'], data['texCoords'], -1)
                os.remove(f"cache/vbo_add/{file}")
            except:
                continue
        
        try:
            # Get player position
            position = self.player.state['position']
            position = (int(position[0]) // Chunk.SIZE[0], int(position[1]) // Chunk.SIZE[1], int(position[2]) // Chunk.SIZE[2])
            for x in range(-self.RENDER_DISTANCE, self.RENDER_DISTANCE + 1):
                for z in range(-self.RENDER_DISTANCE, self.RENDER_DISTANCE + 1):
                    chunk_pos = [
                        int(position[0] + x),
                        int(0),
                        int(position[2] + z)
                    ]
                    _chunk_pos = position_to_string(chunk_pos)
                    if not _chunk_pos in list(self.chunks.keys()):
                        self.to_generate.append(chunk_pos)
            
            # Remove chunks that are too far away
            for chunk in self.chunks:
                _chunk = string_to_position(chunk)
                if abs(position[0] - _chunk[0]) > self.RENDER_DISTANCE or abs(position[2] - _chunk[2]) > self.RENDER_DISTANCE:
                    self.chunks[chunk]._destroy()
                    del self.chunks[chunk]
        except RuntimeError:
            pass
        
        if self.n % 8 == 0:
            if len(self.to_generate) > 0:
                chunk = self.to_generate[-1]
                self.generate_chunk(chunk)
                self.to_generate.remove(chunk)
                
        # Get the chunks which are not visible to the player
        rot = self.player.state['rotation']
        chunks_not_visible = []
        FOV = 100 # Field of view
        for chunk in self.chunks:
            # Get the chunk position
            chunk_pos = string_to_position(chunk)
            # Get the angle
            angle = math.degrees(math.atan2(chunk_pos[2] - position[2], chunk_pos[0] - position[0]))
            # Get the difference
            diff = angle + rot[1] + 90
            if diff > FOV / 2 or diff < -FOV / 2:
                chunks_not_visible.append(chunk)
        for chunk in self.chunks:
            self.chunks[chunk].show()
        for i in chunks_not_visible:
            self.chunks[i].hide()
            
        # Show all chunks within the render distance / 4
        for chunk in self.chunks:
            dist = math.dist(position, string_to_position(chunk))
            if dist > self.RENDER_DISTANCE * Chunk.SIZE[0] / 4:
                self.chunks[chunk].hide()
            else:
                self.chunks[chunk].show()