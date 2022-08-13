import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from core.fileutils import *
from core.util import *
from core.renderer import TerrainMeshStorage
from models import cube, slab, add_position


try:
    os.mkdir("cache/")
except FileExistsError:
    pass

listener = ListenerBase('cache/vbo_request/')
writer   = WriterBase('cache/vbo/')
writer2  = WriterBase('cache/')

def _block_exists(dict, position):
    return position in dict

def get_texcoords(data, id):
    for item in data.items():
        if item[1]["id"] == id:
            return item[1]["texture_coords"]

while True:
    for i in listener.queue:
        try:
            item = listener.get_queue_item(i)
            if item is not None:
                blocks = item["blocks"]
                _blocks = {}
                for index, block in blocks.items():
                    _blocks[tuple(decode_position(index))] = block
                blocks = _blocks

                chunk_position = decode_position(item["position"])
                block_types = item["block_types"]

                storage = TerrainMeshStorage()

                for position, block in blocks.items():
                    x, y, z = list(position)
                    position = (x, y, z)
                    texcoords = get_texcoords(block_types, block)
                    
                    if not _block_exists(blocks, (x, y + 1, z)):
                        storage.add(add_position(position, cube.vertices["top"]), texcoords["top"])

                    if not _block_exists(blocks, (x, y - 1, z)):
                        storage.add(add_position(position, cube.vertices["bottom"]), texcoords["bottom"])

                    if not _block_exists(blocks, (x - 1, y, z)):
                        storage.add(add_position(position, cube.vertices["left"]), texcoords["left"])

                    if not _block_exists(blocks, (x + 1, y, z)):
                        storage.add(add_position(position, cube.vertices["right"]), texcoords["right"])

                    if not _block_exists(blocks, (x, y, z - 1)):
                        storage.add(add_position(position, cube.vertices["front"]), texcoords["front"])

                    if not _block_exists(blocks, (x, y, z + 1)):
                        storage.add(add_position(position, cube.vertices["back"]), texcoords["back"])

                data = storage._group()

                for data_item in data:
                    writer.write("AUTO", {
                        "vertices": data_item[0],
                        "texCoords": data_item[1],
                    })

        except ValueError:
            pass