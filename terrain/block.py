from OpenGL.GL import *
import threading
import random

def execute_with_delay(func, delay):
    threading.Thread(target=lambda: threading.Timer(delay, func).start(), daemon=True).start()

class Block:
    """
    Block
    * Base block class
    """
    def __init__(self, name, renderer):
        """
        Block.__init__
        :name: name of the block
        :texture: texture of the block
        :parent: the parent window
        """
        self.name = name
        self.renderer = renderer
        self.tex_coords = {}
        self.preloads = []
        self.preloads_per_frame = 1
        self.preloaded = 0
        
        self.added_data = []

    def preload(self, position, chunk):
        """
        preload
        * Preloads the textures of the block
        """
        self.preloads.append((position, chunk))

    def add(self, position, chunk):
        """
        add
        * Adds a block to the world
        :position: the position of the block
        """

        x, y, z = position
        X, Y, Z = (x + 1, y + 1, z + 1)

        face_ids = {}

        if not chunk.block_exists((x, Y, z)):
            face_ids["top"] = execute_with_delay(lambda: self.renderer.add((x, Y, Z,  X, Y, Z,  X, Y, z,  x, Y, z), self.tex_coords["top"]), random.randrange(1, 2))
        if not chunk.block_exists((x, y - 1, z)):
            face_ids["bottom"] = execute_with_delay(lambda: self.renderer.add((x, y, z, X, y, z, X, y, Z, x, y, Z), self.tex_coords["bottom"]), random.randrange(1, 2))
        if not chunk.block_exists((x - 1, y, z)):
            face_ids["left"] = execute_with_delay(lambda: self.renderer.add((x, y, z,  x, y, Z,  x, Y, Z,  x, Y, z), self.tex_coords["left"]), random.randrange(1, 2))
        if not chunk.block_exists((X, y, z)):
            face_ids["right"] = execute_with_delay(lambda: self.renderer.add((X, y, Z,  X, y, z,  X, Y, z,  X, Y, Z), self.tex_coords["right"]), random.randrange(1, 2))
        if not chunk.block_exists((x, y, Z)):
            face_ids["front"] = execute_with_delay(lambda: self.renderer.add((x, y, Z,  X, y, Z,  X, Y, Z,  x, Y, Z), self.tex_coords["front"]), random.randrange(1, 2))
        if not chunk.block_exists((x, y, z - 1)):
            face_ids["back"] = execute_with_delay(lambda: self.renderer.add((X, y, z,  x, y, z,  x, Y, z,  X, Y, z), self.tex_coords["back"]), random.randrange(1, 2))

        self.added_data.append({
            "position": position,
            "chunk": chunk,
            "face_ids": face_ids # To make urgent draw calls, e.g. when the player breaks a block
        })

    def _add(self, position, chunk):
        """
        add
        * Adds a block to the world, from a preload
        :position: the position of the block
        """

        x, y, z = position
        X, Y, Z = (x + 1, y + 1, z + 1)

        face_ids = {}

        if not chunk.block_exists((x, Y, z)):
            face_ids["top"] = self.renderer.add((x, Y, Z,  X, Y, Z,  X, Y, z,  x, Y, z), self.tex_coords["top"])
        if not chunk.block_exists((x, y - 1, z)):
            face_ids["bottom"] = self.renderer.add((x, y, z, X, y, z, X, y, Z, x, y, Z), self.tex_coords["bottom"])
        if not chunk.block_exists((x - 1, y, z)):
            face_ids["left"] = self.renderer.add((x, y, z,  x, y, Z,  x, Y, Z,  x, Y, z), self.tex_coords["left"])
        if not chunk.block_exists((X, y, z)):
            face_ids["right"] = self.renderer.add((X, y, Z,  X, y, z,  X, Y, z,  X, Y, Z), self.tex_coords["right"])
        if not chunk.block_exists((x, y, Z)):
            face_ids["front"] = self.renderer.add((x, y, Z,  X, y, Z,  X, Y, Z,  x, Y, Z), self.tex_coords["front"])
        if not chunk.block_exists((x, y, z - 1)):
            face_ids["back"] = self.renderer.add((X, y, z,  x, y, z,  x, Y, z,  X, Y, z), self.tex_coords["back"])
        self.added_data.append({
            "position": position,
            "chunk": chunk,
            "face_ids": face_ids # To make urgent draw calls, e.g. when the player breaks a block
        })
        # if len(list(face_ids.values())) > 0:
        #     self.preloaded += 1

    def process_preloads(self):
        """
        process_preloads
        * Processes the preloads
        """
        i = 0
        while i < 2:
            try:
                position, chunk = self.preloads.pop(0)
                threading.Thread(target=lambda: self._add(position, chunk), daemon=True).start()
                i = self.preloaded
            except IndexError:
                break
            self.preloaded = 0
class GrassBlock(Block):
    def __init__(self, renderer):
        super().__init__("grass", renderer)
        self.tex_coords = {
            "top": self.renderer.texture_manager.texture_coords["grass.png"],
            "bottom": self.renderer.texture_manager.texture_coords["dirt.png"],
            "left": self.renderer.texture_manager.texture_coords["grass_side.png"],
            "right": self.renderer.texture_manager.texture_coords["grass_side.png"],
            "front": self.renderer.texture_manager.texture_coords["grass_side.png"],
            "back": self.renderer.texture_manager.texture_coords["grass_side.png"]
        }

class DirtBlock(Block):
    def __init__(self, renderer):
        super().__init__("dirt", renderer)
        self.tex_coords = {
            "top": self.renderer.texture_manager.texture_coords["dirt.png"],
            "bottom": self.renderer.texture_manager.texture_coords["dirt.png"],
            "left": self.renderer.texture_manager.texture_coords["dirt.png"],
            "right": self.renderer.texture_manager.texture_coords["dirt.png"],
            "front": self.renderer.texture_manager.texture_coords["dirt.png"],
            "back": self.renderer.texture_manager.texture_coords["dirt.png"]
        }

class StoneBlock(Block):
    def __init__(self, renderer):
        super().__init__("stone", renderer)
        self.tex_coords = {
            "top": self.renderer.texture_manager.texture_coords["stone.png"],
            "bottom": self.renderer.texture_manager.texture_coords["stone.png"],
            "left": self.renderer.texture_manager.texture_coords["stone.png"],
            "right": self.renderer.texture_manager.texture_coords["stone.png"],
            "front": self.renderer.texture_manager.texture_coords["stone.png"],
            "back": self.renderer.texture_manager.texture_coords["stone.png"]
        }

class SandBlock(Block):
    def __init__(self, renderer):
        super().__init__("sand", renderer)
        self.tex_coords = {
            "top": self.renderer.texture_manager.texture_coords["sand.png"],
            "bottom": self.renderer.texture_manager.texture_coords["sand.png"],
            "left": self.renderer.texture_manager.texture_coords["sand.png"],
            "right": self.renderer.texture_manager.texture_coords["sand.png"],
            "front": self.renderer.texture_manager.texture_coords["sand.png"],
            "back": self.renderer.texture_manager.texture_coords["sand.png"]
        }
