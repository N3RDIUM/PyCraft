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
from core import logger
from models import add_position
from core.utils import string_to_position, position_to_string
from terrain.chunk import Chunk
import pyfastnoisesimd as fns
import opensimplex

# Load the blocks from ../../terrain/blocks/blocks.pickle
blocks = pickle.load(open("../../terrain/blocks/blocks.pickle", 'rb'))

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
            try:
                request = json.loads(open_pcdt(f"../../cache/requests/{request}"))
                if request['type'] == "generate-chunk":
                    os.remove(f"../../cache/requests/{request['position']}.pcdt")
                    logger.info(f"[ChunkLoader] Processing request {request}")
                else:
                    continue
            except:
                continue
            _oldpos = request['position']
            request['position'] = string_to_position(request['position'])
            
            # Generate all blocks first
            logger.info(f"[ChunkLoader] Generating blocks for chunk at {_oldpos}")
            _blocks = {}
            _simulated_blocks = {}
            size = Chunk.SIZE
            position = list(request['position'])
            for index in range(len(position)):
                position[index] *= size[index]
                position[index] = int(position[index])
            
            shape = (size[0] + 3, size[1], size[2] + 3)
            offset = (1, 0, 1)
            offset = (offset[0] + position[0], offset[1] + position[1], offset[2] + position[2])
            noisevals = fns.Noise(seed=0, numWorkers=8).genAsGrid(shape=shape, start=offset)
            for x in range(position[0] - 1, position[0] + size[0] + 2):
                for z in range(position[2] - 1, position[2] + size[2] + 2):
                    if x < position[0] + 1 or x > position[0] + size[0] or z < position[2] + 1 or z > position[2] + size[2]:
                        _ = True
                    else:
                        _ = False
                    # Get the height of the terrain at this position
                    height = abs(int(opensimplex.noise2(x / 10, z / 10) * 10)) + 128
                    dirt_height = height - abs(int(opensimplex.noise2(x / 10, z / 10) * 16))
                    # Iterate through the height
                    for y in range(position[1] - 1, height + 1):
                        blocktype = None
                        if y == height:
                            if abs(noisevals[x - position[0] + 1, y - position[1], z - position[2] + 1]) < 0.6:
                                blocktype = "_internals/grass_block"
                        elif y > dirt_height:
                            if abs(noisevals[x - position[0] + 1, y - position[1], z - position[2] + 1]) < 0.55:
                                blocktype = "_internals/dirt"
                        else:
                            if abs(noisevals[x - position[0] + 1, y - position[1], z - position[2] + 1]) < 0.5:
                                blocktype = "_internals/stone"
                        if blocktype is not None:   
                            if _:
                                _simulated_blocks[position_to_string((x, y, z))] = 0
                            else:
                                _blocks[position_to_string((x, y, z))] = blocktype
            
            # Now generate the vertices and texture coordinates
            logger.info(f"[ChunkLoader] Generating vertices and texture coordinates for chunk at {_oldpos}")
            X = 2048 * 3
            Y = 2048 * 2
            vertices = [[]]
            texCoords = [[]]
            block_positions = set(list(_blocks.keys()) + list(_simulated_blocks.keys()))

            # Define the positions of all neighboring blocks
            neighbors = [(0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)]
            facenames = ["top", "bottom", "right", "left", "back", "front"]

            for index, blocktype in _blocks.items():
                idx = string_to_position(index)
                v = blocks[blocktype].details["model"].vertices
                t = blocks[blocktype].details["texture"]
                for neighbor, facename in zip(neighbors, facenames):
                    _n = add_position(neighbor, idx)
                    _n = [int(n) for n in _n]
                    _n = position_to_string(_n)
                    if not _n in block_positions:
                        vertices[-1].extend(add_position(idx, v[facename]))
                        texCoords[-1].extend(t[facename])
                if len(vertices[-1]) > X:
                    vertices.append([])
                if len(texCoords[-1]) > Y:
                    texCoords.append([])
                    
            # Now return the vertices and texture coordinates
            logger.info(f"[ChunkLoader] Saving chunk at {_oldpos}")
            result = json.dumps({
                "type": "chunk",
                "position": _oldpos,
                "blocks": _blocks
            })
            save_pcdt(f"../../cache/results/{_oldpos}.pcdt", result)         
            
            # Group the vertices and texture coordinates into a list
            logger.info(f"[ChunkLoader] Transferring vertices and texture coordinates for chunk at {_oldpos}")
            batches = []
            for index in range(len(vertices)):
                try:
                    tex = texCoords[index]
                except:
                    tex = []
                batches.append({
                    "id": f"{_oldpos}",
                    "request_id": f"{_oldpos}-{index}",
                    "vertices": vertices[index],
                    "texCoords": tex,
                })
            # Save the batches
            for batch in batches:
                save_pcdt(f"../../cache/vbo_add/{batch['request_id']}.pcdt", json.dumps(batch))