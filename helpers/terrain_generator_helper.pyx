import random
from cython.parallel import prange

cdef func_exec(func):
    cdef int n
    with nogil:
        for n in prange(0, 1):
            with gil:
                func()

def _start_generation(world):
    random_index = world._queue[random.randint(0, len(world._queue) - 1)]
    world.all_chunks[random_index].generate()
    world._queue.remove(random_index)

def start_world_generation(world):
    func_exec(lambda: _start_generation(world))
