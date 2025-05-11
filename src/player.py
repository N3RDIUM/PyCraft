import math
import glfw
from core.state import State

class Player:
    """
    Player

    The player class for PyCraft.
    """

    def __init__(self, state: State):
        """
        Initialize the player.

        :param window: The window object.
        :param world: The world object.
        """
        # Set properties
        self.state: State = state
        self.state.player = self

        # Lock mouse pointer
        self.lock = True
        glfw.set_input_mode(self.state.window.window,
                            glfw.CURSOR, glfw.CURSOR_DISABLED)

        # Default state
        self.state_map = {
            "mouse_delta": [0, 0],
            "position": [0, 0, -10],
            "rotation": [0, -180, 0],
            "velocity": [0, 0, 0],
            "friction": 0.9,
            "gravity": 9.81,
            "speed": 0.03,
            "zoom": False,
            "fly": False,
        }

    def drawcall(self):
        """
        Update the player on drawcall.
        """
        # Get the state
        sens = self.state_map["speed"]
        rotY = math.radians(-self.state_map["rotation"][1])
        dx, dz = math.sin(rotY), math.cos(rotY)

        # Key handlers
        if glfw.get_key(self.state.window.window, glfw.KEY_S) == glfw.PRESS:
            self.state_map["velocity"][0] += dx*sens
            self.state_map["velocity"][2] -= dz*sens
        if glfw.get_key(self.state.window.window, glfw.KEY_W) == glfw.PRESS:
            self.state_map["velocity"][0] -= dx*sens
            self.state_map["velocity"][2] += dz*sens
        if glfw.get_key(self.state.window.window, glfw.KEY_D) == glfw.PRESS:
            self.state_map["velocity"][0] -= dz*sens
            self.state_map["velocity"][2] -= dx*sens
        if glfw.get_key(self.state.window.window, glfw.KEY_A) == glfw.PRESS:
            self.state_map["velocity"][0] += dz*sens
            self.state_map["velocity"][2] += dx*sens
        if glfw.get_key(self.state.window.window, glfw.KEY_LEFT_CONTROL) == glfw.PRESS:
            self.state_map["speed"] = 0.05
        else:
            self.state_map["speed"] = 0.03

        # ESC to release mouse
        if glfw.get_key(self.state.window.window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_input_mode(self.state.window.window,
                                glfw.CURSOR, glfw.CURSOR_NORMAL)
            self.lock = False
        # L to lock mouse
        if glfw.get_key(self.state.window.window, glfw.KEY_L) == glfw.PRESS:
            glfw.set_input_mode(self.state.window.window,
                                glfw.CURSOR, glfw.CURSOR_DISABLED)
            self.lock = True

        # mouse rotation: get dx and dy
        if self.lock:
            current_position = glfw.get_cursor_pos(self.state.window.window)
            dx = current_position[0] - self.state_map["mouse_delta"][0]
            dy = current_position[1] - self.state_map["mouse_delta"][1]
            dy = -dy  # invert y
            self.state_map["rotation"][0] += dy/8  # pitch
            self.state_map["rotation"][1] -= dx/8  # yaw
            if self.state_map["rotation"][0] > 90:  # clamp pitch
                self.state_map["rotation"][0] = 90
            elif self.state_map["rotation"][0] < -90:  # clamp pitch
                self.state_map["rotation"][0] = -90
            self.state_map["mouse_delta"] = current_position  # update mouse delta

        # SHIFT to fly down
        if glfw.get_key(self.state.window.window, glfw.KEY_SPACE) == glfw.PRESS:
            self.state_map["velocity"][1] -= 0.05
        # SPACE to fly up
        if glfw.get_key(self.state.window.window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
            self.state_map["velocity"][1] += 0.05

        self.state_map["position"][0] += self.state_map["velocity"][0]
        self.state_map["position"][1] += self.state_map["velocity"][1]
        self.state_map["position"][2] += self.state_map["velocity"][2]

        # Apply friction
        self.state_map["velocity"][0] *= self.state_map["friction"]
        self.state_map["velocity"][1] *= self.state_map["friction"]
        self.state_map["velocity"][2] *= self.state_map["friction"]

        # Do the thing
        rot = [self.state_map["rotation"][i] * -1 for i in range(3)]
        self.state.camera.position = self.state_map["position"]
        self.state.camera.rotation = rot

