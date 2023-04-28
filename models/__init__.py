from core import logger

import importlib
import pickle
import os

class Model:
    def __init__(self):
        self.id = "_internals/default"
        self.vertices = {}

def add_position(position, vertices):
    vertices = list(vertices)
    for i in range(0, len(vertices), 3):
        vertices[i] += position[0]
        vertices[i+1] += position[1]
        vertices[i+2] += position[2]
    return vertices

logger.info("[PyCraft] Loading models...")
models = {}
to_load = []
for file in os.listdir(os.path.dirname(__file__)):
    if file.endswith(".py") and not file.startswith("__"):
        to_load.append(file[:-3])
for path in to_load:
    module = importlib.import_module("models." + path)
    model = module._Export()
    models[model.id] = model
    del module
logger.info("[PyCraft] Loaded %d models. Saving to pickle..." % len(models))
pickle.dump(models, open(os.path.join(os.path.dirname(__file__), "models.pickle"), "wb"))
logger.info("[PyCraft] Saved models to pickle.")