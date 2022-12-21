# imports
from core import Window, logger
from terrain import World

# Initialize
logger.info("[PyCraft] Initializing...")
window = Window()
world = World(window=window)
window.schedule_mainloop(world)

if __name__ == "__main__":
    logger.info("[PyCraft] Starting mainloop...")
    window.mainloop()  # Start the mainloop
