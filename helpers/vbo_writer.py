from http import server
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
server_writer  = WriterBase('cache/flaskserver/')

def _block_exists(dict1, dict2, position):
    return position in dict1 or position in dict2

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
                simulated_blocks = item["simulated_blocks"]

                chunk_position = decode_position(item["position"])
                block_types = item["block_types"]
                blockdata = {}

                storage = TerrainMeshStorage()

                for position, block in blocks.items():
                    x, y, z = decode_position(position)
                    position = (x, y, z)
                    texcoords = get_texcoords(block_types, block)
                    encoded_position = encode_position(position)

                    blockdata[encoded_position] = {
                        "type": block,
                        "vertices": [],
                        "texcoords": [],
                    }
                    
                    if not _block_exists(blocks, simulated_blocks, encode_position((x, y + 1, z))):
                        vertices = add_position(position, cube.vertices["top"])
                        _texcoords = texcoords["top"]
                        storage.add(vertices, _texcoords)
                        blockdata[encoded_position]["vertices"].extend(vertices)
                        blockdata[encoded_position]["texcoords"].extend(_texcoords)

                    if not _block_exists(blocks, simulated_blocks, encode_position((x, y - 1, z))):
                        vertices = add_position(position, cube.vertices["bottom"])
                        _texcoords = texcoords["bottom"]
                        storage.add(vertices, _texcoords)
                        blockdata[encoded_position]["vertices"].extend(vertices)
                        blockdata[encoded_position]["texcoords"].extend(_texcoords)

                    if not _block_exists(blocks, simulated_blocks, encode_position((x - 1, y, z))):
                        vertices = add_position(position, cube.vertices["left"])
                        _texcoords = texcoords["left"]
                        storage.add(vertices, _texcoords)
                        blockdata[encoded_position]["vertices"].extend(vertices)
                        blockdata[encoded_position]["texcoords"].extend(_texcoords)

                    if not _block_exists(blocks, simulated_blocks, encode_position((x + 1, y, z))):
                        vertices = add_position(position, cube.vertices["right"])
                        _texcoords = texcoords["right"]
                        storage.add(vertices, _texcoords)
                        blockdata[encoded_position]["vertices"].extend(vertices)
                        blockdata[encoded_position]["texcoords"].extend(_texcoords)

                    if not _block_exists(blocks, simulated_blocks, encode_position((x, y, z - 1))):
                        vertices = add_position(position, cube.vertices["front"])
                        _texcoords = texcoords["front"]
                        storage.add(vertices, _texcoords)
                        blockdata[encoded_position]["vertices"].extend(vertices)
                        blockdata[encoded_position]["texcoords"].extend(_texcoords)

                    if not _block_exists(blocks, simulated_blocks, encode_position((x, y, z + 1))):
                        vertices = add_position(position, cube.vertices["back"])
                        _texcoords = texcoords["back"]
                        storage.add(vertices, _texcoords)
                        blockdata[encoded_position]["vertices"].extend(vertices)
                        blockdata[encoded_position]["texcoords"].extend(_texcoords)

                data = storage._group()

                for data_item in data:
                    writer.write("AUTO", {
                        "vertices": data_item[0],
                        "texCoords": data_item[1],
                    })

                server_writer.write(f"{item['position']}", {
                    "vertices": storage.vertices,
                    "texCoords": storage.texCoords,
                    "blocks": json.dumps(blockdata),
                    "chunk": {
                        "position": item["position"],
                    },
                })

        except ValueError:
            pass