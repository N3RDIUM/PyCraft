import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from settings import *
from terrain.biomes import *
from core.util import encode_vector, decode_vector
from core.fileutils import ListenerBase, WriterBase
from core.logger import *
from core.mesh_storage import TerrainMeshStorage
from models import add_position
from json import JSONDecodeError
from terrain.weather import *
from models import add_position

class ChunkGenerator(ListenerBase):
    def __init__(self):
        log("ChunkGenerator", "Initializing...")
        super().__init__("cache/chunk/")
        self.writer = WriterBase("cache/chunk_build/")
        self.flask_writer = WriterBase("cache/flask/")
        self.vbo_writer = WriterBase("cache/vbo/")
    
    @staticmethod
    def block_exists(dict1, dict2, position):
        position = encode_vector(position)
        if position in dict1:
            return True
        elif position in dict2:
            return True
        else:
            return False

    def on(self, data):
        try:
            _simulated_blocks = {}
            _blocks           = {}

            blocktypes = data["blocktypes"]
            vbo_id     = data["id"]
            position   = data["position"]
            position   = [position[0] * CHUNK_SIZE, position[1] * CHUNK_SIZE]
            seed       = data["seed"]

            SEED = seed

            for x in range(-1, CHUNK_SIZE + 1):
                for z in range(-1, CHUNK_SIZE + 1):
                    weather = get_weather_at((position[0] + x, position[1] + z), SEED)
                    generator = compute_biome(weather, generators)
                    if x == -1 or x == CHUNK_SIZE or z == -1 or z == CHUNK_SIZE:
                        pos = [
                            position[0] + x,
                            position[1] + z
                        ]
                        generator.generate_subchunk(pos, SEED, _simulated_blocks)
                    else:
                        pos = [
                            position[0] + x,
                            position[1] + z
                        ]
                        generator.generate_subchunk(pos, SEED, _blocks)


            data = {
                "id"          : vbo_id,
                "position"    : position,
                "blocktypes"  : blocktypes,
                "blocks"      : _blocks,
                "simulated"   : _simulated_blocks
            }
            log("ChunkGenerator", f"Generated chunk {position} with {len(_blocks)} blocks.")

            blocktypes       = data["blocktypes"]
            vbo_id           = data["id"]
            position         = data["position"]
            position         = (position[0], position[1])
            blocks           = data["blocks"]
            simulated_blocks = data["simulated"]
            block_vbo_data   = {}
            mesh = TerrainMeshStorage()

            for _position, blocktype in blocks.items():
                x, y, z = decode_vector(_position)
                vertices = blocktypes[blocktype]["model"]
                texture  = blocktypes[blocktype]["texture"]

                block_vbo_data[_position] = {
                    "vertices": [],
                    "texCoords": [],
                }

                if not self.block_exists(blocks, simulated_blocks, (x, y + 1, z)):
                    mesh.add(add_position((x, y, z), vertices["top"]), texture["top"])
                    block_vbo_data[_position]["vertices"].extend(add_position((x, y, z), vertices["top"]))
                    block_vbo_data[_position]["texCoords"].extend(texture["top"])
                if not self.block_exists(blocks, simulated_blocks, (x, y - 1, z)):
                    mesh.add(add_position((x, y, z), vertices["bottom"]), texture["bottom"])
                    block_vbo_data[_position]["vertices"].extend(add_position((x, y, z), vertices["bottom"]))
                    block_vbo_data[_position]["texCoords"].extend(texture["bottom"])
                if not self.block_exists(blocks, simulated_blocks, (x + 1, y, z)):
                    mesh.add(add_position((x, y, z), vertices["right"]), texture["right"])
                    block_vbo_data[_position]["vertices"].extend(add_position((x, y, z), vertices["right"]))
                    block_vbo_data[_position]["texCoords"].extend(texture["right"])
                if not self.block_exists(blocks, simulated_blocks, (x - 1, y, z)):
                    mesh.add(add_position((x, y, z), vertices["left"]), texture["left"])
                    block_vbo_data[_position]["vertices"].extend(add_position((x, y, z), vertices["left"]))
                    block_vbo_data[_position]["texCoords"].extend(texture["left"])
                if not self.block_exists(blocks, simulated_blocks, (x, y, z - 1)):
                    mesh.add(add_position((x, y, z), vertices["front"]), texture["front"])
                    block_vbo_data[_position]["vertices"].extend(add_position((x, y, z), vertices["front"]))
                    block_vbo_data[_position]["texCoords"].extend(texture["front"])
                if not self.block_exists(blocks, simulated_blocks, (x, y, z + 1)):
                    mesh.add(add_position((x, y, z), vertices["back"]), texture["back"])
                    block_vbo_data[_position]["vertices"].extend(add_position((x, y, z), vertices["back"]))
                    block_vbo_data[_position]["texCoords"].extend(texture["back"])

            data = mesh._group()

            for data_item in range(len(data)):
                _data_item = data[data_item]
                self.vbo_writer.write(f"{self.writer.written}-vbo_" + str(vbo_id) + "_part_" + str(data_item), {
                    "id": vbo_id,
                    "vertices": _data_item[0],
                    "texCoords": _data_item[1],
                })

            log("ChunkGenerator", f"Chunk {position} has been built.")

            self.flask_writer.write(encode_vector(position), {
                "id": vbo_id,
                "blocks": blocks,
                "simulated": simulated_blocks,
                "vbo_data": block_vbo_data,
            })
            log("ChunkGenerator", f"Chunk {position} has been transferred to the Flask ferver frocess.")     
        except Exception as e:
            log("ChunkGenerator", f"Error while generating chunk: {e}")

if __name__ == "__main__":
    try:
        generator = ChunkGenerator()
        while True:
            if len(generator.queue) > 0:
                try:
                    generator.on(generator.get_last_item())
                except JSONDecodeError:
                    warn("ChunkGenerator", "Invalid JSON data received, skipping...")
                except Exception as e:
                    log("ChunkGenerator", f"Error while generating chunk: {e}")
    except FileNotFoundError:
        pass
    sys.exit()
