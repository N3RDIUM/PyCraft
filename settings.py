import psutil

DEV_MODE = True
DISABLE_CHUNK_CULLING = False
USING_GRAPHICS_DEBUGGER = False
CHUNK_SIZE = 16
CHUNK_GENERATORS = psutil.cpu_count(logical=False)
VERTICES_SIZE = 256 * 16 * 16 * 8 * 24
TEXCOORDS_SIZE = 256 * 16 * 16 * 8 * 16
MIN_FPS = 30
FPS_SAMPLES = 1000
