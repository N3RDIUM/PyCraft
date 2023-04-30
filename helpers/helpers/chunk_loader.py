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
import threading

# Load the blocks from ../../terrain/blocks/blocks.pickle
blocks = pickle.load(open("../../terrain/blocks/blocks.pickle", 'rb'))

def block_exists(position, _blocks, _simulated_blocks):
    position = [int(position[0]), int(position[1]), int(position[2])]
    if position_to_string(position) in list(_blocks):
        return True
    if position_to_string(position) in list(_simulated_blocks):
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
            def _handle(request):
                try:
                    request = json.loads(open_pcdt(f"../../cache/requests/{request}"))
                    if request['type'] == "generate-chunk":
                        os.remove(f"../../cache/requests/{request['position']}.pcdt")
                    else:
                        return
                except:
                    return
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
                
                shape = (size[0] + 3, size[1], size[2] + 3)
                offset = (1, 0, 1)
                offset = (offset[0] + position[0], offset[1] + position[1], offset[2] + position[2])
                noisevals = fns.Noise(seed=0, numWorkers=8).genAsGrid(shape=shape, start=offset)
                for x in tqdm.trange(position[0] - 1, position[0] + size[0] + 2, desc=f"Generating blocks for chunk at {position[0]}, {position[1]}, {position[2]}"):
                    for z in range(position[2] - 1, position[2] + size[2] + 2):
                        if x < position[0] + 1 or x > position[0] + size[0] or z < position[2] + 1 or z > position[2] + size[2]:
                            _ = True
                        else:
                            _ = False
                        # Get the height of the terrain at this position
                        height = abs(int(opensimplex.noise2(x / 10, z / 10) * 10)) + 16
                        # Iterate through the height
                        for y in range(position[1] - 1, height + 1):
                            if y == height:
                                blocktype = "_internals/grass"
                            elif y < height and y > height - 15:
                                blocktype = "_internals/dirt"
                            elif y < height - 15:
                                if noisevals[x - position[0] + 1][y - position[1]][z - position[2] + 1] < 0.2:
                                    blocktype = "_internals/stone"
                            if _:
                                _simulated_blocks[position_to_string((x, y, z))] = 0
                            else:
                                _blocks[position_to_string((x, y, z))] = blocktype
                
                # Then generate the vertices and texture coorinates
                vertices = []
                texCoords = []
                for index, blocktype in tqdm.tqdm(_blocks.items(), desc=f"Generating vertices for chunk at {position[0]}, {position[1]}, {position[2]}"):
                    idx = string_to_position(index)
                    v = blocks[blocktype].details["model"]
                    t = blocks[blocktype].details["texture"]
                    if not block_exists((idx[0], idx[1] + 1, idx[2]), _blocks.keys(), _simulated_blocks.keys()):
                        vertices.extend(add_position(idx, v.vertices["top"]))
                        texCoords.extend(t["top"])
                    if not block_exists((idx[0], idx[1] - 1, idx[2]), _blocks.keys(), _simulated_blocks.keys()):
                        vertices.extend(add_position(idx, v.vertices["bottom"]))
                        texCoords.extend(t["bottom"])
                    if not block_exists((idx[0] + 1, idx[1], idx[2]), _blocks.keys(), _simulated_blocks.keys()):
                        vertices.extend(add_position(idx, v.vertices["right"]))
                        texCoords.extend(t["right"])
                    if not block_exists((idx[0] - 1, idx[1], idx[2]), _blocks.keys(), _simulated_blocks.keys()):
                        vertices.extend(add_position(idx, v.vertices["left"]))
                        texCoords.extend(t["left"])
                    if not block_exists((idx[0], idx[1], idx[2] - 1), _blocks.keys(), _simulated_blocks.keys()):
                        vertices.extend(add_position(idx, v.vertices["front"]))
                        texCoords.extend(t["front"])
                    if not block_exists((idx[0], idx[1], idx[2] + 1), _blocks.keys(), _simulated_blocks.keys()):
                        vertices.extend(add_position(idx, v.vertices["back"]))
                        texCoords.extend(t["back"])
                    
                # Now return the vertices and texture coordinates
                result = json.dumps({
                    "type": "chunk",
                    "position": _oldpos,
                    "blocks": _blocks
                })
                save_pcdt(f"../../cache/results/{_oldpos}.pcdt", result)
                
                # Split the data into batches of X vertices, Y texture coordinates
                X = 16384 * 3
                Y = 16384 * 2
                vertices = [vertices[i:i + X] for i in range(0, len(vertices), X)]
                texCoords = [texCoords[i:i + Y] for i in range(0, len(texCoords), Y)]
                # Group the vertices and texture coordinates into a list
                batches = []
                for index in range(len(vertices)):
                    batches.append({
                        "id": f"{_oldpos}",
                        "request_id": f"{_oldpos}-{index}",
                        "vertices": vertices[index],
                        "texCoords": [],
                    })
                for index in range(len(texCoords)):
                    batches[index]["texCoords"] = texCoords[index]
                # Save the batches
                for batch in batches:
                    save_pcdt(f"../../cache/vbo_add/{batch['request_id']}.pcdt", json.dumps(batch))
        threading.Thread(target=_handle, args=(request,)).start()