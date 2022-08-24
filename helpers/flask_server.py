import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from flask import Flask, jsonify
import json

from core.util import *

app = Flask(__name__)
DIRECTORY = "cache/flaskserver/"

def request_file(chunk_position):
    position = encode_position(chunk_position)
    try:
        with open(f"{DIRECTORY}{position}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

@app.route("/chunk/<chunk_position>")
def chunk_data(chunk_position):
    if chunk_position is None:
        return jsonify({"error": "chunk_position is missing"}), 400
    
    chunk_position = decode_position(chunk_position)
    data = request_file(chunk_position)

    if data is None:
        return jsonify({"exists": False}), 200
    else:
        return jsonify({
            "exists": True,
            "chunk": json.loads(data)
        }), 200

@app.route("/block/<chunk_position>/<block_position>")
def block(chunk_position, block_position):
    if chunk_position is None:
        return jsonify({"error": "chunk_position is missing"}), 400

    if block_position is None:
        return jsonify({"error": "block_position is missing"}), 400

    chunk_position = decode_position(chunk_position)
    data = request_file(chunk_position)
    blocks = data["blocks"] if data is not None else {}

    block = blocks[block_position] if block_position in blocks else None

    if block is None:
        return jsonify({"exists": False}), 200
    else:
        return jsonify({
            "exists": True,
            "block": block,
        }), 200

if __name__ == "__main__":
    app.run(debug=True)
