import json

from core.pcdt import *
from core.utils import position_to_string, string_to_position

class Chunk:
    """
    Chunk
    
    A terrain chunk class for PyCraft.
    It is a 64x64x64 block of terrain.
    """
    SIZE = (64, 64, 64)
    def __init__(self, parent, position):
        self.parent = parent
        self.position = position
        self.renderer = self.parent.renderer
        
        # Create a VBO for the chunk
        self.buffer_id = position_to_string(self.position)
        self.renderer.create_buffer(self.buffer_id)
        
    def generate(self):
        request = json.dumps({
            "type": "generate-chunk",
            "position": self.buffer_id
        })
        save_pcdt(f"cache/requests/{self.buffer_id}.pcdt", request)