import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import flask
from flask import request, jsonify
from core.logger import *
from core.util import encode_position, decode_position
from json import JSONDecodeError
from multiprocessing import Process
from constants import *
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True
info("Flask", "Initializing...")

@app.route('/', methods=['GET'])
def home():
    return "<h1>PyCraft</h1><p>This is a PyCraft server.</p>"

@app.route('/api/v1/chunk', methods=['GET'])
def api_chunk():
    if 'position' in request.args:
        position = decode_position(request.args['position'])
        try:
            with open(f"cache/flask/{encode_position(position)}.json", "r") as f:
                data = json.load(f)
                return jsonify(data)
        except FileNotFoundError:
            return jsonify({
                "error": "Chunk not found."
            })
    else:
        return jsonify({
            "error": "No position provided."
        })

@app.route('/api/v1/block_exists', methods=['GET'])
def api_block_exists():
    if 'position' in request.args:
        block = request.args['position']
        chunk = decode_position(block)
        chunk = [chunk[0] // CHUNK_SIZE, chunk[2] // CHUNK_SIZE]
        chunk = [chunk[0] * CHUNK_SIZE, chunk[1] * CHUNK_SIZE]
        try:
            with open(f"cache/flask/{encode_position(chunk)}.json", "r") as f:
                data = json.load(f)
                if block in data["blocks"]:
                    return jsonify({
                        "exists": True,
                        "block": data["blocks"][block]
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
    else:
        return jsonify({
            "error": "No position provided."
        })

if __name__ == "__main__":
    app.run(port="5079")
