import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from core.fileutils import *
from core.util import *
from constants import CHUNK_SIZE
from helpers.biomes import *

import opensimplex

try:
    os.mkdir("cache/")
except FileExistsError:
    pass

listener = ListenerBase('cache/requested/')
writer   = WriterBase('cache/generated/')
vbo_writer = WriterBase('cache/vbo_request/')

def generate_subchunk(x, y, NOISE, _blocks):
    if NOISE.noise2(x / 160, y / 160) < 0.5:
        blockdata = plains.generate_subchunk(x, y, NOISE)
    else:
        blockdata = desert.generate_subchunk(x, y, NOISE)
    
    if blockdata is not None:
        for position, data in blockdata.items():
            _blocks[position] = data


def generate_chunk(position, seed):
    position = decode_position(position)
    _blocks = {}
    _simulated_blocks = {}
    noise = opensimplex.OpenSimplex(seed=seed)
    for i in range(-1, CHUNK_SIZE + 1):
        for j in range(-1, CHUNK_SIZE + 1):
            if not i == -1 and not i == CHUNK_SIZE and not j == -1 and not j == CHUNK_SIZE:
                generate_subchunk(i + position[0], j + position[1], noise, _blocks)
            else:
                generate_subchunk(i + position[0], j + position[1], noise, _simulated_blocks)

    return [_blocks, _simulated_blocks]

while True:
    try:
        item = listener.get_random_item()
        if item is not None:
            blocks = generate_chunk(item['position'], item['seed'])
            writer.write(f"chunk{item['position']}", {
                'blocks': blocks[0],
            })
            vbo_writer.write(f"chunk{item['position']}", {
                'blocks': blocks[0],
                'simulated_blocks': blocks[1],
                'position': item['position'],
                'block_types': item['blocktypes'],
                "vbo_id": item['vbo_id']
            })
    except ValueError:
        pass
