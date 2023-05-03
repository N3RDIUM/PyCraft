# imports
from OpenGL.GL import *

from core import Player, Renderer, TextureAtlas, logger
from core.pcdt import open_pcdt
from terrain.chunk import Chunk
from misc import Sky
import multiprocessing
processes = multiprocessing.cpu_count()
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
    RENDER_DISTANCE = 5
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
        self.to_generate = []
        self.generate()
        
    def generate_chunk(self, position):
        new = Chunk(self, position)
        self.chunks[tuple(new.position)] = new
        new.generate()
        
    def generate(self):
        for x in range(-self.RENDER_DISTANCE, self.RENDER_DISTANCE + 1):
            for z in range(-self.RENDER_DISTANCE, self.RENDER_DISTANCE + 1):
                self.to_generate.append([x, 0, z])
        
    def drawcall(self):
        """
        Draw the world.
        """
        self.texture_manager.bind(self.texid)
        self.sky.drawcall()  # Draw the sky
        self.player.drawcall()  # Update the player
        self.renderer.drawcall()  # Draw the renderer
        
    def chunk_exists(self, position):
        return tuple(position) in list(self.chunks.keys())
    def chunk_requested(self, position):
        return list(position) in self.to_generate
    
    def block_exists(self, position):
        chunkpos = (int(position[0]) // Chunk.SIZE[0], 0, int(position[2]) // Chunk.SIZE[2])
        try:
            return self.chunk_exists(chunkpos) and self.chunks[chunkpos].block_exists(position)
        except:
            return False
        
    def check_collision(self, position):
        position = [int(position[0]), int(position[1]), int(position[2])]
        neighbors = [
            # Typical block neighbors
            (0, 1, 0), 
            (0, -2, 0), 
            
            (1, 0, 0), 
            (1, -1, 0),
            (-1, 0, 0), 
            (-1, -1, 0),
            
            (0, 0, 1),
            (0, -1, 1), 
            (0, 0, -1),
            (0, -1, -1)
        ]
        results = [False]*10
        for neighbor in neighbors:
            if self.block_exists((position[0] + neighbor[0], position[1] + neighbor[1], position[2] + neighbor[2])):
                results[neighbors.index(neighbor)] = True
            else:
                results[neighbors.index(neighbor)] = False
        return results
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
            # Remove chunks that are too far away
            for _chunk in self.chunks:
                if abs(position[0] - _chunk[0]) > self.RENDER_DISTANCE or abs(position[2] - _chunk[2]) > self.RENDER_DISTANCE:
                    self.chunks[_chunk]._destroy()
                    del self.chunks[_chunk]
                    logger.info(f"[World] Unloading chunk at {_chunk}")
            for _chunk in self.to_generate:
                if abs(position[0] - _chunk[0]) > self.RENDER_DISTANCE or abs(position[2] - _chunk[2]) > self.RENDER_DISTANCE:
                    self.to_generate.remove(_chunk)
                    logger.info(f"[World] Cancelling chunk load request at {_chunk}")
            # Add chunks according to player position, if they don't exist
            to_add = []
            for x in range(-self.RENDER_DISTANCE, self.RENDER_DISTANCE + 1):
                for z in range(-self.RENDER_DISTANCE, self.RENDER_DISTANCE + 1):
                    if not self.chunk_exists((position[0] + x, 0, position[2] + z)) and not self.chunk_requested((position[0] + x, 0, position[2] + z)):
                        to_add.append([position[0] + x, 0, position[2] + z])
            self.to_generate += to_add
            self.to_generate.sort(key=lambda x: math.sqrt((x[0] - position[0]) ** 2 + (x[2] - position[2]) ** 2))
        except RuntimeError:
            pass
        
        # Sort to_generate by distance to player
        self.to_generate.sort(key=lambda x: math.sqrt((x[0] - position[0]) ** 2 + (x[2] - position[2]) ** 2))
        
        # Generate chunks in queue
        if self.n % 4 == 0:
            if len(self.to_generate) > 0:
                time.sleep((self.RENDER_DISTANCE)/(60-self.RENDER_DISTANCE))
                for i in range(processes // 8):
                    chunk = self.to_generate.pop(0)
                    self.generate_chunk(chunk)
                    logger.info(f"[World] Generated chunk at {chunk}")
                
        # Get the chunks which are not visible to the player
        rot = self.player.state['rotation']
        chunks_not_visible = []
        FOV = 100 # Field of view
        for chunk_pos in self.chunks:
            # Get the angle
            angle = math.degrees(math.atan2(chunk_pos[2] - position[2], chunk_pos[0] - position[0]))
            # Get the difference
            diff = angle + rot[1] + 90
            if diff > FOV / 2 or diff < -FOV / 2:
                chunks_not_visible.append(chunk_pos)
        for chunk in self.chunks:
            self.chunks[chunk].show()
        for i in chunks_not_visible:
            self.chunks[i].hide()
            
        # Show all chunks within the 2 chunk radius
        for chunk in self.chunks:
            dist = math.dist(position, chunk)
            if dist > self.RENDER_DISTANCE:
                self.chunks[chunk].hide()
            else:
                self.chunks[chunk].show()