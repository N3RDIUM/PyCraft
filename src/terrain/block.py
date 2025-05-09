import numpy as np

# BUG: FACES ARE INVERTED (FRONT IS BACK, BACK IS FRONT ETC)
# WHICH IS WHY WE ARE HAVING TO TRANSLATE WITH +1 IN CHUNK.PY

back = np.array([
    0, 1, 0,
    1, 1, 0,
    0, 0, 0,
    
    1, 0, 0,
    0, 0, 0,
    1, 1, 0,
], dtype = np.float32)

left = np.array([
    1, 1, 0,
    1, 1, 1,
    1, 0, 0,

    1, 0, 1,
    1, 0, 0,
    1, 1, 1,
], dtype = np.float32)

front = np.array([
    1, 1, 1,
    0, 1, 1,
    1, 0, 1,

    0, 0, 1,
    1, 0, 1,
    0, 1, 1,
], dtype = np.float32)

right = np.array([
    0, 1, 1,
    0, 1, 0,
    0, 0, 1,

    0, 0, 0,
    0, 0, 1,
    0, 1, 0,
], dtype = np.float32)

bottom = np.array([
    0, 1, 1,
    1, 1, 1,
    0, 1, 0,

    1, 1, 0,
    0, 1, 0,
    1, 1, 1,
], dtype = np.float32)

top = np.array([
    0, 0, 0,
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

