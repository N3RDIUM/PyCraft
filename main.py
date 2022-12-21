# imports
from core import Window, logger

# Initialize
logger.info("[PyCraft] Initializing...")
window = Window()

if __name__ == "__main__":
    logger.info("[PyCraft] Starting mainloop...")
    window.mainloop()  # Start the mainloop
