import numpy as np

front = np.array([
    0, 1, 0, # Front
    1, 1, 0,
    0, 0, 0,
    
    1, 1, 0,
    1, 0, 0,
    0, 0, 0,
], dtype = np.float32)

right = np.array([
    1, 1, 0, # Right
    1, 1, 1,
    1, 0, 0,

    1, 0, 1,
    1, 0, 0,
    1, 1, 1,
], dtype = np.float32)

back = np.array([
    1, 1, 1, # Back
    0, 1, 1,
    1, 0, 1,

    0, 0, 1,
    1, 0, 1,
    0, 1, 1,
], dtype = np.float32)

left = np.array([
    0, 1, 1, # Left
    0, 1, 0,
    0, 0, 1,

    0, 0, 0,
    0, 0, 1,
    0, 1, 0,
], dtype = np.float32)

top = np.array([
    0, 1, 1, # Top
    1, 1, 1,
    0, 1, 0,

    1, 1, 0,
    0, 1, 0,
    1, 1, 1,
], dtype = np.float32)

bottom = np.array([
    0, 0, 0, # Bottom
    1, 0, 0,
    0, 0, 1,

    1, 0, 1,
    0, 0, 1,
    1, 0, 0,
], dtype = np.float32)

uv = np.array([
    0, 0,
    1, 0,
    0, 1,

    1, 1,
    0, 1,
    1, 0,
], dtype = np.float32)

