import random

def start_generaion(world):
    random_index = world._queue[random.randint(0, len(world._queue) - 1)]
    world.all_chunks[random_index].generate()
    world._queue.remove(random_index)
