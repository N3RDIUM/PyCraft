from pyglet.window import key
from pyglet.gl import *
import math
from Box2D import *


def polar_to_cartesian(radius, angle):
    return [radius * math.cos(angle), radius * math.sin(angle)]


def cartesian_to_polar(x, y):
    return math.sqrt(x**2 + y**2), math.atan2(y, x)

class _collision_engine:
    def __init__(self, player):
        self.player = player
        self._block_size = 1
        self.player_diameter = 0.75

    def _collision_algorithm(self, player_pos, block_pos):
        if block_pos[0] - player_pos[0] <= self.player_diameter-0.1/2 + self._block_size-0.1/2 or player_pos[1] - block_pos[1] <= self.player_diameter-0.1/2 + self._block_size-0.1/2:
            return False
        else:
            return True

    def step(self):
        player_x = self.player.pos[0]-int(self.player.pos[0])
        player_y = self.player.pos[1]-int(self.player.pos[1])
        player_z = self.player.pos[2]-int(self.player.pos[2])

        # Facing north
        if self.player.rot[1] > 360-45 and self.player.rot[1] < 45:
            if self.player.block_exists["forward"]:
                if self._collision_algorithm(self.player.pos, [player_x, player_y, player_z-1]):
                    self.player.movable["forward"] = False
                else:
                    self.player.movable["forward"] = True
            
            if self.player.block_exists["backward"]:
                if self._collision_algorithm(self.player.pos, [player_x, player_y, player_z+1]):
                    self.player.movable["backward"] = False
                else:
                    self.player.movable["backward"] = True

            if self.player.block_exists["left"]:
                if self._collision_algorithm(self.player.pos, [player_x+1, player_y, player_z]):
                    self.player.movable["left"] = False
                else:
                    self.player.movable["left"] = True

            if self.player.block_exists["right"]:
                if self._collision_algorithm(self.player.pos, [player_x-1, player_y, player_z]):
                    self.player.movable["right"] = False
                else:
                    self.player.movable["right"] = True

def _to_radians(angle):
    return angle * math.pi / 180

def normalize(position):
    """ Accepts `position` of arbitrary precision and returns the block
    containing that position.
    Parameters
    ----------
    position : tuple of len 3
    Returns
    -------
    block_position : tuple of ints of len 3
    """
    x, y, z = position
    x, y, z = (int(round(x)), int(round(y)), int(round(z)))
    return (x, y, z)

class Player:
    def __init__(self, pos=(0, 0, 0), rot=(0, 0), parent=None):
        self.pos = list(pos)
        self.rot = list(rot)
        self.x = 0
        self.y = 0
        self.z = 0
        self.rotY = 0
        self.rotX = 0
        self.parent = parent
        self.speed = 0.3
        self.pointing_at = [[0,0,0], [0,0,0]]

        self.block_exists = {"left": False, "right": False,
                             "forward": False, "backward": False, "up": False, "down": False}
        self.movable = {"left": True, "right": True, "forward": True,
                        "backward": True, "up": True, "down": True}
        self.suffocating = False
        self.falling = False
        self.velocity_y = 0
        self.gravity = 0.02
        self.hit_range = 8

        self.terminal_velocity = 5

        self._listener = _collision_engine(self)
        self.mouse_click = False

    def mouse_motion(self, dx, dy):
        self.rot[0] += dy/8
        self.rot[1] -= dx/8
        if self.rot[0] > 90:
            self.rot[0] = 90
        elif self.rot[0] < -90:
            self.rot[0] = -90
        self.rot[0] = self.rot[0]
        self.rot[1] = self.rot[1]

    def collide(self):
        x_int = int(self.pos[0])
        y_int = int(self.pos[1])
        z_int = int(self.pos[2])

        if not self.parent.model.block_exists((x_int-1, y_int-1, z_int)) or self.parent.model.block_exists((x_int-1, y_int-2, z_int)):
            self.block_exists["left"] = False
        else:
            self.block_exists["left"] = True

        if self.parent.model.block_exists((x_int+1, y_int-1, z_int)) or self.parent.model.block_exists((x_int+1, y_int-2, z_int)):
            self.block_exists["right"] = False
        else:
            self.block_exists["right"] = True

        if not self.parent.model.block_exists((x_int, y_int-1, z_int-1)) or self.parent.model.block_exists((x_int, y_int-2, z_int-1)):
            self.block_exists["backward"] = False
        else:
            self.block_exists["backward"] = True

        if not self.parent.model.block_exists((x_int, y_int-1, z_int+1)) or self.parent.model.block_exists((x_int, y_int-2, z_int+1)):
            self.block_exists["forward"] = False
        else:
            self.block_exists["forward"] = True

        if self.parent.model.block_exists((x_int, y_int-3, z_int)):
            self.falling = False
            self.velocity_y = 0
        else:
            self.falling = True
            self.velocity_y -= self.gravity

    def hit_test(self, position, vector, max_distance=8):
        m = 8
        x, y, z = position
        dx, dy, dz = vector
        previous = None
        for _ in range(max_distance * m):
            key = normalize((x, y, z))
            if key != previous and self.parent.model.block_exists(key):
                self.pointing_at[0] = key
                self.pointing_at[1] = previous
                return key, previous
            previous = key
            x, y, z = x + dx / m, y + dy / m, z + dz / m
        self.pointing_at[0] = None
        self.pointing_at[1] = None
        return None, None

    def update(self, dt, keys):
        sens = self.speed
        s = dt*10
        rotY = _to_radians(-self.rot[1])
        rotX = _to_radians(-self.rot[0])
        dx, dz = math.sin(rotY), math.cos(rotY)

        _dx, _dz = s*math.sin(rotX), math.cos(rotY)
        self.hit_test(self.pos, (_dx, _dz, 0), self.hit_range)
        
        self.collide()
        self._listener.step()
        if self.velocity_y > self.terminal_velocity:
            self.velocity_y = self.terminal_velocity
        if self.velocity_y < -self.terminal_velocity:
            self.velocity_y = -self.terminal_velocity

        if keys[key.W] and self.movable["forward"]:
            self.pos[0] += dx*sens
            self.pos[2] -= dz*sens
        if keys[key.S] and self.movable["backward"]:
            self.pos[0] -= dx*sens
            self.pos[2] += dz*sens
        if keys[key.A] and self.movable["left"]:
            self.pos[0] -= dz*sens
            self.pos[2] -= dx*sens
        if keys[key.D] and self.movable["right"]:
            self.pos[0] += dz*sens
            self.pos[2] += dx*sens
        if keys[key.SPACE] and self.movable["up"] and not self.suffocating and not self.falling:
            self.velocity_y += 0.2
        if keys[key.LCTRL]:
            self.speed = 0.5
        else:
            self.speed = 0.3

        if self.mouse_click and not self.pointing_at[0] is None and not self.pointing_at[1] is None:
            if self.parent.model.block_exists([self.pointing_at[0][0], self.pointing_at[0][1], self.pointing_at[0][2]]):
                self.parent.model.remove_block([self.pointing_at[0][0], self.pointing_at[0][1], self.pointing_at[0][2]])

        self.pos[1] += self.velocity_y

        self.x = self.pos[0]
        self.y = self.pos[2]
        self.z = self.pos[1]

        self.rotY = self.rot[0]
        self.rotX = self.rot[1]
