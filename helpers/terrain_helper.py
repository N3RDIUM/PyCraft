from multiprocessing import Manager

if __name__ == '__main__':
    manager = Manager()
    l = manager.list()
    manager.register('TerrainGen')

    class RenderThread:
        def __init__(self):
            self.manager = manager
            self.l = manager.list()

        def work(self):
            for chunk in self.l:
                chunk.add_to_batch()
