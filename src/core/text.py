# imports
import sys

from OpenGL.GL import glPushMatrix, glPopMatrix, glWindowPos2f
from OpenGL.GLUT import glutInit, glutBitmapCharacter, GLUT_BITMAP_8_BY_13

glutInit(sys.argv)  # Initialize glut


def text(position, text):
    """
    Draw text on the screen.

    :param position: The position of the text.
    :param text: The text to draw.
    """
    x, y = position
    glPushMatrix()
    glWindowPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(char))
    glPopMatrix()


def display_debug(position, array):
    """
    Display debug information.

    :param position: The position of the text.
    :param array: The array of text to display.
    """
    array = array[::-1]
    array = array[:32]
    position = list(position)
    for i, line in enumerate(array):
        text(position, line)
        position[1] += 10