from OpenGL.GL import *
from OpenGL.GLUT import *
import sys

glutInit(sys.argv)

def text(x, y, text):
    glPushMatrix()
    glWindowPos2f(x, y)
    glutBitmapString(GLUT_BITMAP_TIMES_ROMAN_24, text.encode('ascii'))
    glPopMatrix()