x, y, z = 0, 0, 0
X, Y, Z = 1, 1, 1

vertices = {
    "top": (x, Y, Z,  X, Y, Z,  X, Y, z,  x, Y, z),
    "bottom": (x, y, z,  X, y, z,  X, y, Z,  x, y, Z),
    "left": (x, y, z,  x, y, Z,  x, Y, Z,  x, Y, z),
    "right": (X, y, Z,  X, y, z,  X, Y, z,  X, Y, Z),
    "front": (x, y, Z,  X, y, Z,  X, Y, Z,  x, Y, Z),
    "back": (X, y, z,  x, y, z,  x, Y, z,  X, Y, z),
}