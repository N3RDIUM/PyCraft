from core import logger

import os
import pickle
import importlib

blocks = {}

logger.info("[PyCraft] Loading blocks...")
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

logger.info("[PyCraft] Loaded %d blocks. Loading block models..." % len(blocks))
from models import models
for block in blocks.values():
    model = block.details["model"]
    try:
        block.details["model"] = models[model]
    except:
        logger.warning("[PyCraft] Block %s has an invalid model: %s" % (block.details["id"], model))

logger.info("[PyCraft] Loaded %d blocks. Loading block texture coords..." % len(blocks))
# Load texture pickle at assets/textures/textures.pickle
texcoords = pickle.load(open("assets/textures/textures.pickle", "rb"))
for block in blocks.values():
    texture = block.details["texture"]
    for i in texture:
        texture[i] = texcoords[texture[i]]
    block.details["texture"] = texture
    
logger.info("[PyCraft] Loaded %d blocks. Saving to pickle..." % len(blocks))

# Pickle the blocks for later use
pickle.dump(blocks, open(os.path.join(os.path.join(os.path.dirname(__file__), "blocks"), "blocks.pickle"), "wb"))
logger.info("[PyCraft] Saved blocks to pickle.")