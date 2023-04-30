import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import time
import json
import pickle

from core.pcdt import *
from models import add_position
from core.utils import string_to_position, position_to_string
from terrain.chunk import Chunk

# Load the blocks from ../../terrain/blocks/blocks.pickle
blocks = pickle.load(open("../../terrain/blocks/blocks.pickle", 'rb'))

def block_exists(position, _blocks, _simulated_blocks):
    if position_to_string(position) in _blocks or position_to_string(position) in _simulated_blocks:
        return True
    return False 

# Start generating chunks
while True:
    # Listen for all requests in the cache
    requests = os.listdir("../../cache/requests")
    
    # If there are no requests, sleep
    if len(requests) == 0:
        time.sleep(1)
        continue
    # Otherwise, process the requests
    else:
        for request in requests:
            request = json.loads(open_pcdt(f"../../cache/requests/{request}"))
            if request['type'] == "generate-chunk":
                os.remove(f"../../cache/requests/{request['position']}.pcdt")
            else:
                continue
            _oldpos = request['position']
            request['position'] = string_to_position(request['position'])
            
            # Generate all blocks first
            _blocks = {}
            _simulated_blocks = {}
            size = Chunk.SIZE
            position = list(request['position'])
            for index in range(len(position)):
                position[index] *= size[index]
                position[index] = int(position[index])
            
            for x in range(position[0] - 1, position[0] + size[0] + 1):
                for y in range(size[1]):
                    for z in range(position[2] - 1, position[2] + size[2] + 1):
                        if x == position[0] - 1 or x == position[0] + size[0] or z == position[2] - 1 or z == position[2] + size[2]:
                            _simulated_blocks[position_to_string((x, y, z))] = '_internals/dirt'
                        else:
                            _blocks[position_to_string((x, y, z))] = '_internals/dirt'
            
            # Then generate the vertices and texture coorinates
            vertices = []
            texCoords = []
            for index, blocktype in _blocks.items():
                idx = string_to_position(index)
                if not block_exists((idx[0], idx[1] + 1, idx[2]), _blocks, _simulated_blocks):
                    vertices.extend(add_position(idx, blocks[blocktype].details["model"].vertices["top"]))
                    texCoords.extend(blocks[blocktype].details["texture"]["top"])
                if not block_exists((idx[0], idx[1] - 1, idx[2]), _blocks, _simulated_blocks):
                    vertices.extend(add_position(idx, blocks[blocktype].details["model"].vertices["bottom"]))
                    texCoords.extend(blocks[blocktype].details["texture"]["bottom"])
                if not block_exists((idx[0] + 1, idx[1], idx[2]), _blocks, _simulated_blocks):
                    vertices.extend(add_position(idx, blocks[blocktype].details["model"].vertices["right"]))
                    texCoords.extend(blocks[blocktype].details["texture"]["right"])
                if not block_exists((idx[0] - 1, idx[1], idx[2]), _blocks, _simulated_blocks):
                    vertices.extend(add_position(idx, blocks[blocktype].details["model"].vertices["left"]))
                    texCoords.extend(blocks[blocktype].details["texture"]["left"])
                if not block_exists((idx[0], idx[1], idx[2] + 1), _blocks, _simulated_blocks):
                    vertices.extend(add_position(idx, blocks[blocktype].details["model"].vertices["front"]))
                    texCoords.extend(blocks[blocktype].details["texture"]["front"])
                if not block_exists((idx[0], idx[1], idx[2] - 1), _blocks, _simulated_blocks):
                    vertices.extend(add_position(idx, blocks[blocktype].details["model"].vertices["back"]))
                    texCoords.extend(blocks[blocktype].details["texture"]["back"])
                
            # Now return the vertices and texture coordinates
            result = json.dumps({
                "type": "chunk",
                "position": _oldpos,
                "vertices": vertices,
                "texCoords": texCoords,
                "blocks": _blocks
            })
            save_pcdt(f"../../cache/results/{_oldpos}.pcdt", result)