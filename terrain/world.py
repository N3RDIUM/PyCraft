# imports
from misc import Sky
from core import logger, Player

from OpenGL.GL import *  # Import OpenGL

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
        glEnable(GL_DEPTH_TEST)  # Enable depth testing
        glEnable(GL_CULL_FACE)  # Enable culling
        
        glBegin(GL_QUADS)  # Begin drawing quads
        glColor3f(0.0, 1.0, 0.0)  # Set the color to green
        
        # Draw the front face
        glVertex3f(-1.0, -1.0, 1.0)
        glVertex3f(1.0, -1.0, 1.0)
        glVertex3f(1.0, 1.0, 1.0)
        glVertex3f(-1.0, 1.0, 1.0)

        # Draw the back face
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(-1.0, 1.0, -1.0)
        glVertex3f(1.0, 1.0, -1.0)
        glVertex3f(1.0, -1.0, -1.0)
    
        # Draw the top face
        glVertex3f(-1.0, 1.0, -1.0)
        glVertex3f(-1.0, 1.0, 1.0)
        glVertex3f(1.0, 1.0, 1.0)
        glVertex3f(1.0, 1.0, -1.0)

        # Draw the bottom face
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(1.0, -1.0, -1.0)
        glVertex3f(1.0, -1.0, 1.0)
        glVertex3f(-1.0, -1.0, 1.0)

        # Draw the right face
        glVertex3f(1.0, -1.0, -1.0)
        glVertex3f(1.0, 1.0, -1.0)
        glVertex3f(1.0, 1.0, 1.0)
        glVertex3f(1.0, -1.0, 1.0)
        
        # Draw the left face
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(-1.0, -1.0, 1.0)
        glVertex3f(-1.0, 1.0, 1.0)
        glVertex3f(-1.0, 1.0, -1.0)
        
        glEnd()  # End drawing quads
