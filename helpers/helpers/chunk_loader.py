import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import tqdm
import time
import json
import pickle

from core.pcdt import *
from models import add_position
from core.utils import string_to_position, position_to_string
from terrain.chunk import Chunk
import pyfastnoisesimd as fns
import opensimplex

# Load the blocks from ../../terrain/blocks/blocks.pickle
blocks = pickle.load(open("../../terrain/blocks/blocks.pickle", 'rb'))

def block_exists(position, _blocks, _simulated_blocks):
    position = [int(position[0]), int(position[1]), int(position[2])]
    if position_to_string(position) in list(_blocks) or position in list(_simulated_blocks):
        return True
    else:
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
            
            shape = (size[0] + 2, size[1], size[2] + 2)
            offset = (1, 0, 1)
            offset = (offset[0] + position[0], offset[1] + position[1], offset[2] + position[2])
            noisevals = fns.Noise(seed=0, numWorkers=8).genAsGrid(shape=shape, start=offset,)
            for x in tqdm.trange(position[0] - 1, position[0] + size[0] + 1, desc=f"Generating blocks for chunk at {position[0]}, {position[1]}, {position[2]}"):
                for z in range(position[2] - 1, position[2] + size[2] + 1):
                    # Get the height of the terrain at this position
                    height = abs(int(opensimplex.noise2(x / 1000, z / 1000) * 100)) + 10
                    # Iterate through the height
                    for y in range(position[1] - 1, height + 1):
                        blocktype = "_internals/stone"
                        if y == height:
                            blocktype = "_internals/grass"
                        elif y < height and y > height - 5:
                            blocktype = "_internals/dirt"
                        elif y < height - 5:
                            if noisevals[x - position[0] + 1][y - position[1]][z - position[2] + 1] < 0.5:
                                blocktype = "_internals/stone"
                        # Add the block to the _blocks dictionary
                        _blocks[position_to_string((x, y, z))] = blocktype        
            
            # Then generate the vertices and texture coorinates
            vertices = []
            texCoords = []
            for index, blocktype in tqdm.tqdm(_blocks.items(), desc=f"Generating vertices for chunk at {position[0]}, {position[1]}, {position[2]}"):
                idx = string_to_position(index)
                if not block_exists((idx[0], idx[1] + 1, idx[2]), _blocks.keys(), _simulated_blocks.keys()):
                    vertices.extend(add_position(idx, blocks[blocktype].details["model"].vertices["top"]))
                    texCoords.extend(blocks[blocktype].details["texture"]["top"])
                if not block_exists((idx[0], idx[1] - 1, idx[2]), _blocks.keys(), _simulated_blocks.keys()):
                    vertices.extend(add_position(idx, blocks[blocktype].details["model"].vertices["bottom"]))
                    texCoords.extend(blocks[blocktype].details["texture"]["bottom"])
                if not block_exists((idx[0] + 1, idx[1], idx[2]), _blocks.keys(), _simulated_blocks.keys()):
                    vertices.extend(add_position(idx, blocks[blocktype].details["model"].vertices["right"]))
                    texCoords.extend(blocks[blocktype].details["texture"]["right"])
                if not block_exists((idx[0] - 1, idx[1], idx[2]), _blocks.keys(), _simulated_blocks.keys()):
                    vertices.extend(add_position(idx, blocks[blocktype].details["model"].vertices["left"]))
                    texCoords.extend(blocks[blocktype].details["texture"]["left"])
                if not block_exists((idx[0], idx[1], idx[2] - 1), _blocks.keys(), _simulated_blocks.keys()):
                    vertices.extend(add_position(idx, blocks[blocktype].details["model"].vertices["front"]))
                    texCoords.extend(blocks[blocktype].details["texture"]["front"])
                if not block_exists((idx[0], idx[1], idx[2] + 1), _blocks.keys(), _simulated_blocks.keys()):
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