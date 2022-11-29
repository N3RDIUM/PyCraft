import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from core.util import decode_position, encode_position
from core.fileutils import ListenerBase, WriterBase
from core.logger import *
from core.mesh_storage import TerrainMeshStorage
from models import add_position

class ChunkBuilder(ListenerBase):
    def __init__(self):
        log("ChunkBuilder", "Initializing...")
        super().__init__("cache/chunk_build/")
        self.writer = WriterBase("cache/vbo/")

    @staticmethod
    def block_exists(dict1, dict2, position):
        position = encode_position(position)
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
            mesh = TerrainMeshStorage()

            for _position, blocktype in blocks.items():
                x, y, z = decode_position(_position)
                vertices = blocktypes[blocktype]["model"]
                texture  = blocktypes[blocktype]["texture"]

                if not self.block_exists(blocks, simulated_blocks, (x, y + 1, z)):
                    mesh.add(add_position((x, y, z), vertices["top"]), texture["top"])
                if not self.block_exists(blocks, simulated_blocks, (x, y - 1, z)):
                    mesh.add(add_position((x, y, z), vertices["bottom"]), texture["bottom"])
                if not self.block_exists(blocks, simulated_blocks, (x + 1, y, z)):
                    mesh.add(add_position((x, y, z), vertices["right"]), texture["right"])
                if not self.block_exists(blocks, simulated_blocks, (x - 1, y, z)):
                    mesh.add(add_position((x, y, z), vertices["left"]), texture["left"])
                if not self.block_exists(blocks, simulated_blocks, (x, y, z - 1)):
                    mesh.add(add_position((x, y, z), vertices["front"]), texture["front"])
                if not self.block_exists(blocks, simulated_blocks, (x, y, z + 1)):
                    mesh.add(add_position((x, y, z), vertices["back"]), texture["back"])

            data = mesh._group()

            for data_item in range(len(data) - 1):
                _data_item = data[data_item]
                self.writer.write("vbo_" + str(vbo_id) + "_part_" + str(data_item), {
                    "id": vbo_id,
                    "vertices": _data_item[0],
                    "texCoords": _data_item[1],
                })

            log("ChunkBuilder", f"Chunk {position} has been built.")
        except:
            pass

if __name__ == "__main__":
    try:
        generator = ChunkBuilder()
        while True:
            if len(generator.queue) > 0:
                try:
                    time.sleep(1)
                    generator.on(generator.get_first_item())
                except PermissionError:
                    pass
                except IndexError:
                    pass
                except:
                    pass
    except FileNotFoundError:
        pass
    exit()
