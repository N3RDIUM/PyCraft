import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from core.util import decode_vector, encode_vector
from core.fileutils import ListenerBase, WriterBase
from core.logger import *
from core.mesh_storage import TerrainMeshStorage
from models import add_position
from json import JSONDecodeError

class ChunkBuilder(ListenerBase):
    def __init__(self):
        log("ChunkBuilder", "Initializing...")
        super().__init__("cache/chunk_build/")
        self.writer = WriterBase("cache/vbo/")
        self.flask_writer = WriterBase("cache/flask/")

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
                self.writer.write("vbo_" + str(vbo_id) + "_part_" + str(data_item), {
                    "id": vbo_id,
                    "vertices": _data_item[0],
                    "texCoords": _data_item[1],
                })

            log("ChunkBuilder", f"Chunk {position} has been built.")

            self.flask_writer.write(encode_vector(position), {
                "id": vbo_id,
                "blocks": blocks,
                "simulated": simulated_blocks,
                "vbo_data": block_vbo_data,
            })
            log("ChunkBuilder", f"Chunk {position} has been transferred to the Flask ferver frocess.")        
        except Exception as e:
            warn("ChunkBuilder", f"Error while building chunk: {e}")

if __name__ == "__main__":
    try:
        generator = ChunkBuilder()
        while True:
            if len(generator.queue) > 0:
                try:
                    generator.on(generator.get_last_item())
                except JSONDecodeError:
                    warn("ChunkBuilder", "Invalid JSON data received, skipping...") 
                except Exception as e:
                    warn("ChunkBuilder", f"Error while building chunk: {e}")           
    except FileNotFoundError:
        pass
    sys.exit()
