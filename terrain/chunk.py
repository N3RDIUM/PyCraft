import os
import json
import threading

from core.pcdt import *
from core.utils import position_to_string, string_to_position

class Chunk:
    """
    Chunk
    
    A terrain chunk class for PyCraft.
    """
    SIZE = (16, 1, 16)
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
        self.thread = threading.Thread(target=self.wait_for_result)
        self.thread.start()
        
    def wait_for_result(self):
        while True:
            results = os.listdir("cache/results")
            for result in results:
                try:
                    data = json.loads(open_pcdt(f"cache/results/{result}"))
                    if data['position'] == self.buffer_id:
                        self.vertices = data['vertices']
                        self.texCoords = data['texCoords']
                        self.blocks = data['blocks']
                        self.parent.scheduled_chunks.append(self.buffer_id)
                        os.remove(f"cache/results/{result}")
                        return
                except:
                    continue