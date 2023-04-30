# imports
import os
import shutil

from core import Window, logger
from terrain import World
from helpers.start_helpers import start_helpers

if __name__ == "__main__":
    # Initialize
    logger.info("[PyCraft] Initializing...")

    if not os.path.isdir("cache"):
        os.mkdir("cache")
    else:
        shutil.rmtree("cache")
        os.mkdir("cache")
        
    if not os.path.isdir("cache/requests"):
        os.mkdir("cache/requests")
    else:
        shutil.rmtree("cache/requests")
        os.mkdir("cache/requests")
        
    if not os.path.isdir("cache/results"):
        os.mkdir("cache/results")
    else:
        shutil.rmtree("cache/results")
        os.mkdir("cache/results")
        
    if not os.path.isdir("cache/vbo_add"):
        os.mkdir("cache/vbo_add")
    else:
        shutil.rmtree("cache/vbo_add")
        os.mkdir("cache/vbo_adds")

    window = Window()
    world = World(window=window)
    window.schedule_mainloop(world)
    window.schedule_shared_context(world)
    
    logger.info("[PyCraft] Starting helpers...")
    start_helpers()
    
    logger.info("[PyCraft] Starting mainloop...")
    window.mainloop()  # Start the mainloop
        