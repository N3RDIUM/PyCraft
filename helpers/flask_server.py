import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import flask
from flask import request, jsonify
from core.logger import *
from core.util import encode_vector, decode_vector, decode_vector_float
from constants import *
from core.fileutils import ListenerBase, WriterBase
import json
import math
import time
import uuid
import threading

app = flask.Flask(__name__)
app.config["DEBUG"] = True
info("Flask", "Initializing...")

@app.route('/', methods=['GET'])
def home():
    return "<h1>PyCraft</h1><p>This is a PyCraft server.</p>"

@app.route('/api/v1/chunk', methods=['GET'])
def api_chunk():
    if 'position' in request.args:
        position = decode_vector(request.args['position'])
        try:
            with open(f"cache/flask/{encode_vector(position)}.json", "r") as f:
                data = json.load(f)
                return jsonify(data)
        except FileNotFoundError:
            return jsonify({
                "error": "Chunk not found."
            })
        except json.JSONDecodeError:
            return jsonify({
                "error": "Chunk file is corrupted.",
            })
    else:
        return jsonify({
            "error": "No position provided."
        })

@app.route('/api/v1/block_exists', methods=['GET'])
def api_block_exists():
    if 'position' in request.args:
        block = request.args['position']
        chunk = decode_vector(block)
        chunk = [chunk[0] // CHUNK_SIZE, chunk[2] // CHUNK_SIZE]
        chunk = [chunk[0] * CHUNK_SIZE, chunk[1] * CHUNK_SIZE]
        try:
            with open(f"cache/flask/{encode_vector(chunk)}.json", "r") as f:
                data = json.load(f)
                if block in data["blocks"]:
                    return jsonify({
                        "exists": True,
                        "block": data["blocks"][block],
                        "position": block,
                        "vbo_data": data["vbo_data"][block]
                    })
                else:
                    return jsonify({
                        "exists": False
                    })
        except FileNotFoundError:
            return jsonify({
                "error": "Chunk not found.",
                "chunk": chunk
            })
        except json.JSONDecodeError:
            return jsonify({
                "error": "Chunk file is corrupted.",
                "chunk": chunk
            })
    else:
        return jsonify({
            "error": "No position provided."
        })
    
@app.route('/api/v1/remove_block', methods=['GET'])
def api_remove_block():
    if 'position' in request.args:
        block = request.args['position']
        chunk = decode_vector(block)
        chunk = [chunk[0] // CHUNK_SIZE, chunk[2] // CHUNK_SIZE]
        chunk = [chunk[0] * CHUNK_SIZE, chunk[1] * CHUNK_SIZE]
        try:
            with open(f"cache/flask/{encode_vector(chunk)}.json", "r") as f:
                data = json.load(f)
                if block in data["blocks"]:
                    del data["blocks"][block]
                    print("Deleted block from chunk.")
                    vbo_data = data["vbo_data"][block]
                    print("Got vbo_data.")
                    del data["vbo_data"][block]
                    print("Deleted vbo_data from chunk.")
                    with open(f"cache/flask/{encode_vector(chunk)}.json", "w") as f:
                        json.dump(data, f)
                    print("Saved chunk.")
                    with open(f"cache/vbo_remove/{encode_vector(chunk)}.json", "w") as f:
                        json.dump({
                            "id": encode_vector(chunk),
                            "vbo_data": vbo_data
                        }, f)
                    print("Saved vbo_data.")
                    return jsonify({
                        "success": True,
                        "position": block,
                        "vbo_data": vbo_data,
                        "chunk": chunk,
                    })
                else:
                    return jsonify({
                        "success": False
                    })
        except FileNotFoundError:
            return jsonify({
                "error": "Chunk not found.",
                "chunk": chunk
            })
        except json.JSONDecodeError:
            return jsonify({
                "error": "Chunk file is corrupted.",
                "chunk": chunk
            })
    else:
        return jsonify({
            "error": "No position provided."
        })

@app.route('/api/v1/get_block_from_view', methods=['GET'])
def api_get_block_from_view():
    if 'position' in request.args and 'rotation' in request.args and 'hitrange' in request.args:
        position = decode_vector_float(request.args['position'])
        rotation = decode_vector_float(request.args['rotation'])
        hitrange = int(request.args['hitrange'])
        print(position, rotation, hitrange)
        
        # Get the 9 surrounding chunks' data
        chunks = []
        for x in range(-1, 2):
            for z in range(-1, 2):
                try:
                    with open(f"cache/flask/{encode_vector([position[0] + x * CHUNK_SIZE, position[2] + z * CHUNK_SIZE])}.json", "r") as f:
                        data = json.load(f)
                        chunks.append(data)
                except FileNotFoundError:
                    pass
                except json.JSONDecodeError:
                    pass

        # Get the block that is being looked at
        block = None
        for i in range(1, hitrange):
            # flip z axis
            x = position[0] + math.sin(math.radians(rotation[1])) * math.cos(math.radians(rotation[0])) * i
            y = position[1] + math.sin(math.radians(rotation[0])) * i
            z = position[2] + math.cos(math.radians(rotation[1])) * math.cos(math.radians(rotation[0])) * i

            # Get the chunk that the block is in
            chunk = [x // CHUNK_SIZE, z // CHUNK_SIZE]

            # Get the block's position in the chunk
            block_position = [x % CHUNK_SIZE, y, z % CHUNK_SIZE]

            # Get the block's position in the world
            block_position_world = [x, y, z]

            # Get the chunk's data
            chunk_data = None
            for c in chunks:
                if c["id"] == encode_vector(chunk):
                    chunk_data = c
                    break

            # Check if the block exists
            if chunk_data is not None:
                if encode_vector(block_position) in chunk_data["blocks"]:
                    block = chunk_data["blocks"][encode_vector(block_position)]
                    break

        if block is not None:
            return jsonify({
                "success": True,
                "block": block,
                "position": encode_vector(block_position_world)
            })
        else:
            return jsonify({
                "success": False
            })
        
def listen_for_new_files():
    writer   = WriterBase("cache/chunk_data_transfer/")
    main_writer = WriterBase("cache/flask/")
    listener = ListenerBase("cache/_flask/")
    while True:
        if listener.get_queue_length() > 0:
            time.sleep(4)
            data = listener.get_first_item()
            _data = data.copy()
            chunkid = data["id"]
            data = json.dumps(data)
            data = [data[i:i+160000] for i in range(0, len(data), 160000)]
            _writer  = WriterBase(f"cache/chunk_data_transfer/{chunkid}/")
            for d in data:
                _writer.write(filename=uuid.uuid4().hex, data={"data":d})
            main_writer.write(filename=chunkid, data=_data)
if __name__ == "__main__":
    listen_for_new_files()
    # app.run(port="2077")