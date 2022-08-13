import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from core.fileutils import *
from core.util import *
from constants import CHUNK_SIZE

import opensimplex

try:
    os.mkdir("cache/")
except FileExistsError:
    pass

listener = ListenerBase('cache/requested/')
writer   = WriterBase('cache/generated/')
vbo_writer = WriterBase('cache/vbo_request/')

def generate_filament(x, y, NOISE, _blocks):
    height_noise = abs(round(NOISE.noise2(x / 16, y / 16) * 10))
    height_noise_low = -(abs(128 + round(NOISE.noise2(x / 16, y / 16) * 10)))

    dirt_noise = abs(5 + round(NOISE.noise2(x / 16, y / 16) * 20))

    _blocks[encode_position((x, height_noise, y))] = 1

    for i in range(height_noise_low, height_noise - 1):
        cave_noise = abs(round(NOISE.noise3(x / 16, i/16, y / 16) * 10))
        if i < height_noise and i > height_noise - dirt_noise:
            if cave_noise < 3:
                _blocks[encode_position((x, i, y))] = 0
        else:
            if cave_noise < 4:
                _blocks[encode_position((x, i, y))] = 2

def generate_chunk(position, seed):
    position = decode_position(position)
    _blocks = {}
    noise = opensimplex.OpenSimplex(seed=seed)
    for i in range(0, CHUNK_SIZE):
        for j in range(0, CHUNK_SIZE):
            generate_filament(i + position[0], j + position[1], noise, _blocks)
    return _blocks

while True:
    for i in listener.queue:
        try:
            item = listener.get_queue_item(i)
            if item is not None:
                blocks = generate_chunk(item['position'], item['seed'])
                writer.write(f"chunk{item['position']}", {
                    'blocks': blocks
                })
                vbo_writer.write(f"chunk{item['position']}", {
                    'blocks': blocks,
                    'position': item['position'],
                    'block_types': item['blocktypes']
                })
        except ValueError:
            pass
