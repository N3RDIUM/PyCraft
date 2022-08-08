# imports
from OpenGL.GL import *
import math
import glfw

# player class
class Player:
    """
    Player

    * the first person controller
    """
    def __init__(self, parent=None):
        """
        Player.__init__

        :pos: the position of the player
        :rot: the rotation of the player
        :parent: the parent of the player
        """
        self.pos = [0, 0, 0]
        self.rot = [0, 0, 0]
        self.vel = [0, 0, 0]
        self.window = parent
        self.speed = 0.03
        self.friction = 0.9

        # lock mouse pointer
        self.lock = True
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        # dx and dy
        self.position_previous = glfw.get_cursor_pos(self.window)
        self.current_position = glfw.get_cursor_pos(self.window)

    def mouse_motion(self, dx, dy):
        """
        mouse_motion

        * handles mouse movement

        :dx: the change in x
        :dy: the change in y
        """
        self.rot[0] += dy/8
        self.rot[1] -= dx/8
        if self.rot[0] > 90:
            self.rot[0] = 90
        elif self.rot[0] < -90:
            self.rot[0] = -90
        self.rot[0] = self.rot[0]
        self.rot[1] = self.rot[1]

    def update(self):
        """
        update

        * updates the player

        :dt: the delta time
        :keys: the keys pressed
        """
        sens = self.speed
        rotY = math.radians(-self.rot[1])
        dx, dz = math.sin(rotY), math.cos(rotY)

        if glfw.get_key(self.window, glfw.KEY_W) == glfw.PRESS:
            self.vel[0] += dx*sens
            self.vel[2] -= dz*sens
        if glfw.get_key(self.window, glfw.KEY_S) == glfw.PRESS:
            self.vel[0] -= dx*sens
            self.vel[2] += dz*sens
        if glfw.get_key(self.window, glfw.KEY_A) == glfw.PRESS:
            self.vel[0] -= dz*sens
            self.vel[2] -= dx*sens
        if glfw.get_key(self.window, glfw.KEY_D) == glfw.PRESS:
            self.vel[0] += dz*sens
            self.vel[2] += dx*sens
        if glfw.get_key(self.window, glfw.KEY_LEFT_CONTROL) == glfw.PRESS:
            self.speed = 0.05
        else:
            self.speed = 0.03

        # ESC to release mouse
        if glfw.get_key(self.window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_NORMAL)
            self.lock = False
        # L to lock mouse
        if glfw.get_key(self.window, glfw.KEY_L) == glfw.PRESS:
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
            self.lock = True
        
        # mouse rotation: get dx and dy
        if self.lock:
            self.current_position = glfw.get_cursor_pos(self.window)
            dx = self.current_position[0] - self.position_previous[0]
            dy = self.current_position[1] - self.position_previous[1]
            self.mouse_motion(dx, -dy)
            self.position_previous = self.current_position

        # SHIFT to fly down
        if glfw.get_key(self.window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
            self.vel[1] -= 0.05
        # SPACE to fly up
        if glfw.get_key(self.window, glfw.KEY_SPACE) == glfw.PRESS:
            self.vel[1] += 0.05

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[2] += self.vel[2]

        self.vel[0] *= self.friction
        self.vel[1] *= self.friction
        self.vel[2] *= self.friction

        self._translate()

    def _translate(self):
        glRotatef(-self.rot[0], 1, 0, 0)
        glRotatef(-self.rot[1], 0, 1, 0)
        glTranslatef(-self.pos[0], -self.pos[1], -self.pos[2])