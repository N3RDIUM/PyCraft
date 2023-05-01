# imports
import math

import glfw
from OpenGL.GL import glRotatef, glTranslatef

from core import logger

##################################################
# Player class                                   #
##################################################


class Player:
    """
    Player

    The player class for PyCraft.
    """

    def __init__(self, window=None, world=None):
        """
        Initialize the player.

        :param window: The window object.
        :param world: The world object.
        """
        logger.info("[Player] Initializing player...")
        # Set properties
        self.window = window
        self.world = world

        # Lock mouse pointer
        self.lock = True
        glfw.set_input_mode(self.window.window,
                            glfw.CURSOR, glfw.CURSOR_DISABLED)

        # Default state
        self.state = {
            "mouse_delta": [0, 0],
            "position": [0, 130, 0],
            "rotation": [0, 0, 0],
            "velocity": [0, 0, 0],
            "friction": 0.9,
            "gravity": 9.81,
            "speed": 0.1,
            "zoom": False,
            "fly": False,
        }

    def drawcall(self):
        """
        Update the player on drawcall.
        """
        # Get the state
        sens = self.state["speed"]
        rotY = math.radians(-self.state["rotation"][1])
        dx, dz = math.sin(rotY), math.cos(rotY)

        # Key handlers
        if glfw.get_key(self.window.window, glfw.KEY_W) == glfw.PRESS:
            self.state["velocity"][0] += dx*sens
            self.state["velocity"][2] -= dz*sens
        if glfw.get_key(self.window.window, glfw.KEY_S) == glfw.PRESS:
            self.state["velocity"][0] -= dx*sens
            self.state["velocity"][2] += dz*sens
        if glfw.get_key(self.window.window, glfw.KEY_A) == glfw.PRESS:
            self.state["velocity"][0] -= dz*sens
            self.state["velocity"][2] -= dx*sens
        if glfw.get_key(self.window.window, glfw.KEY_D) == glfw.PRESS:
            self.state["velocity"][0] += dz*sens
            self.state["velocity"][2] += dx*sens
        if glfw.get_key(self.window.window, glfw.KEY_LEFT_CONTROL) == glfw.PRESS:
            self.state["speed"] = 0.05
        else:
            self.state["speed"] = 0.03

        # ESC to release mouse
        if glfw.get_key(self.window.window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_input_mode(self.window.window,
                                glfw.CURSOR, glfw.CURSOR_NORMAL)
            self.lock = False
        # L to lock mouse
        if glfw.get_key(self.window.window, glfw.KEY_L) == glfw.PRESS:
            glfw.set_input_mode(self.window.window,
                                glfw.CURSOR, glfw.CURSOR_DISABLED)
            self.lock = True

        # mouse rotation: get dx and dy
        if self.lock:
            current_position = glfw.get_cursor_pos(self.window.window)
            dx = current_position[0] - self.state["mouse_delta"][0]
            dy = current_position[1] - self.state["mouse_delta"][1]
            dy = -dy  # invert y
            self.state["rotation"][0] += dy/8  # pitch
            self.state["rotation"][1] -= dx/8  # yaw
            if self.state["rotation"][0] > 90:  # clamp pitch
                self.state["rotation"][0] = 90
            elif self.state["rotation"][0] < -90:  # clamp pitch
                self.state["rotation"][0] = -90
            self.state["mouse_delta"] = current_position  # update mouse delta

        # SHIFT to fly down
        if glfw.get_key(self.window.window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
            self.state["velocity"][1] -= 0.05
        # SPACE to fly up
        if glfw.get_key(self.window.window, glfw.KEY_SPACE) == glfw.PRESS:
            self.state["velocity"][1] += 0.05

        self.state["position"][0] += self.state["velocity"][0]
        self.state["position"][1] += self.state["velocity"][1]
        self.state["position"][2] += self.state["velocity"][2]

        # Apply friction
        self.state["velocity"][0] *= self.state["friction"]
        self.state["velocity"][1] *= self.state["friction"]
        self.state["velocity"][2] *= self.state["friction"]

        # Draw the player
        glRotatef(-self.state["rotation"][0], 1, 0, 0)
        glRotatef(-self.state["rotation"][1], 0, 1, 0)
        glTranslatef(-self.state["position"][0], -
                     self.state["position"][1], -self.state["position"][2])
