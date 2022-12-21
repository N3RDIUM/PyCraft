# imports
from OpenGL.GL import glClearColor

##################################################
# Sky class                                      #
##################################################


class Sky:
    """
    Sky

    The sky class for PyCraft.
    """

    def __init__(self):
        """
        Initialize the sky.
        """
        self.color = (0.5, 0.69, 1.0, 1.0)

    def drawcall(self):
        """
        Draw the sky.
        """
        glClearColor(*self.color)  # Set the clear color
