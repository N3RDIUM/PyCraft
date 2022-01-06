# imports
import pyglet, opensimplex

# Inbuilt imports
import Classes as pycraft

def load_biomes(world):
    """
    load_biomes

    * Loads all biomes
    """
    import os
    import importlib

    _ = {}

    for file in os.listdir("Classes/terrain/biomes"):
        if file.endswith(".py") and file != "__init__.py":
            _[file[:-3].split('.py')[0]] = importlib.import_module("Classes.terrain.biomes." + file[:-3]).Biome(world)
    return _


class Biome:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.noise = opensimplex.OpenSimplex(seed=self.parent.seed)
        self.generated_queue = []
