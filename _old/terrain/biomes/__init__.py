import importlib
import os

generators = {}
for file in os.listdir(os.path.dirname(__file__)):
    if file.endswith(".py") and not file.startswith("__"):
        module = importlib.import_module(f"terrain.biomes.{file[:-3]}")
        generators[file[:-3]] = module.Generator()
