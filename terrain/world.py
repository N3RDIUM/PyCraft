# imports
from misc import Sky
from core import logger, Player

class World:
    """
    World

    The world class for PyCraft.
    """

    def __init__(self, window=None, renderer=None):
        """
        Initialize the world.
        """
        logger.info("[World] Initializing world...")
        # Window and sky properties
        self.window = window
        self.renderer = renderer

        # Initialize
        self.sky = Sky()
        self.player = Player(window=window, world=self)

    def drawcall(self):
        """
        Draw the world.
        """
        self.sky.drawcall() # Draw the sky
        self.player.drawcall() # Update the player
        # self.renderer.drawcall()
