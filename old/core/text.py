from OpenGL.GL import *
from OpenGL.GLUT import *
import sys
from settings import *

glutInit(sys.argv)

def text(position, text):
    x, y = position
    glPushMatrix()
    glWindowPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(char))
    glPopMatrix()

def display_debug(position, array):
    array = array[::-1]
    array = array[:MAX_DEBUG_LINES]
    position = list(position)
    for i, line in enumerate(array):
        text(position, line)
        position[1] += 10