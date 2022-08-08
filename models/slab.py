x, y, z = 0, 0, 0
X, Y, Z = 1, 0.5, 1

vertices = {
    "top": (x, Y, Z,  X, Y, Z,  X, Y, z,  x, Y, z, x, Y, Z, X, Y, z,),
    "bottom": (x, y, z,  X, y, z,  X, y, Z,  x, y, Z, x, y, z, X, y, Z,),
    "left": (x, y, z,  x, y, Z,  x, Y, Z,  x, Y, z, x, y, z, x, Y, Z,),
    "right": (X, y, Z,  X, y, z,  X, Y, z,  X, Y, Z, X, y, Z, X, Y, z,),
    "front": (x, y, Z,  X, y, Z,  X, Y, Z,  x, Y, Z, x, y, Z, X, Y, Z,),
    "back": (X, y, z,  x, y, z,  x, Y, z,  X, Y, z, X, y, z, x, Y, z,),
}