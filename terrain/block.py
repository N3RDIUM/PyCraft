import os
import pickle
import importlib
blocks = {}

# Load all blocks
to_load = []
for file in os.listdir(os.path.join(os.path.dirname(__file__), "blocks")):
    if file.endswith(".py") and not file.startswith("__"):
        to_load.append(file[:-3])
for path in to_load:
    module = importlib.import_module("terrain.blocks." + path)
    block = module._Export()
    blocks[block.details["id"]] = block
    del module

# Pickle the blocks for later use
pickle.dump(blocks, open(os.path.join(os.path.join(os.path.dirname(__file__), "blocks"), "blocks.pickle"), "wb"))
