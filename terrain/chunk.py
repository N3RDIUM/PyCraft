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
    SIZE = (16, 256, 16)
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
                        self.blocks = data['blocks']
                        self.block_positions = list(data['blocks'].keys())
                        for i in range(len(self.block_positions)):
                            self.block_positions[i] = [int(i) for i in string_to_position(self.block_positions[i])]
                        os.remove(f"cache/results/{result}")
                        return
                except:
                    continue
                
    def block_exists(self, position):
        return list(position) in list(self.block_positions)
                
    def _destroy(self):
        self.renderer.remove_buffer(self.buffer_id)
        del self.position
        del self.buffer_id
        
    def show(self):
        self.renderer.buffers[self.buffer_id]["enabled"] = True
    def hide(self):
        self.renderer.buffers[self.buffer_id]["enabled"] = False