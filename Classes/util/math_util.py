import math

def polar_to_cartesian(radius, angle):
    """
    polar_to_cartesian

    * converts polar coordinates to cartesian

    :radius: the radius
    :angle: the angle
    """
    return [radius * math.cos(angle), radius * math.sin(angle)]

def cartesian_to_polar(x, y):
    """
    cartesian_to_polar

    * converts cartesian coordinates to polar

    :x: the x coordinate
    :y: the y coordinate
    """
    return [math.hypot(x**2 + y**2), math.atan2(y, x)]

def normalize(position):
    """
    normalize

    * normalizes a position

    :position: the position
    """
    x, y, z = position
    x, y, z = (int(round(x)), int(round(y)), int(round(z)))
    return (x, y, z)

def distance_vector_2d(x1, y1, x2, y2):
    """
    distance_vector_2d

    * calculates the distance between two points

    :x1: the x coordinate of the first point
    :y1: the y coordinate of the first point
    :x2: the x coordinate of the second point
    :y2: the y coordinate of the second point
    """
    return math.dist([x1, y1], [x2, y2])

def _to_radians(angle):
    """
    _to_radians

    * converts degrees to radians

    :angle: the angle
    """
    return angle * math.pi / 180