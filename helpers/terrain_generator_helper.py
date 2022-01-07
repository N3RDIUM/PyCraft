# import the necessary modules
import pyximport
pyximport.install()
from .shared_pointer_wrapper import get_shared

def start_generaion(world):
    # We don't have to worry about infinite loops, because
    # this is going to be run in another thread, using popen.
    while True:
        for i in world.all_chunks:
            if world.all_chunks[i].generated == False:
                world.all_chunks[i].generate()

if __name__ == "__main__":
    world = get_shared('PyCraftWorld')
    start_generaion(world)
