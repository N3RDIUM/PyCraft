def _vertices(size, position):
    """
    Generates the vertices for a cube.
    """
    x, y, z = position
    X, Y, Z = x + 1, y + 1, z + 1
    vertices = (
        x, Y, Z,  X, Y, Z,  X, Y, z,  x, Y, z,
        x, y, z,  X, y, z,  X, y, Z,  x, y, Z,
        x, y, z,  x, y, Z,  x, Y, Z,  x, Y, z,
        X, y, Z,  X, y, z,  X, Y, z,  X, Y, Z,
        x, y, Z,  X, y, Z,  X, Y, Z,  x, Y, Z,
        X, y, z,  x, y, z,  x, Y, z,  X, Y, z,
    )
    return vertices