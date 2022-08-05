import os
import json
import multiprocessing

class ListenerBase:
    def __init__(self, directory):
        self.directory = directory
        self.process = multiprocessing.Process(target=self.listen)
        self.queue = []
        self.process.start()

    def listen(self):
        while True:
            dir = os.listdir(self.directory)
            for file in dir:
                if file.endswith(".json"):
                    filename = file.split(".json")[0]
                    if not filename in self.queue:
                        self.queue.append(filename)

    def get_queue_item(self, id):
        item = self.queue.pop(id)
        with open(self.directory + item + ".json", "r") as f:
            data = json.load(f)
        return data

    def get_queue_length(self):
        return len(self.queue)

class WriterBase:
    def __init__(self, directory):
        self.directory = directory
        self.process = multiprocessing.Process(target=self.write_process)
        self.write_queue = []
        self.process.start()

    def write_process(self):
        while True:
            if len(self.write_queue) > 0:
                item = self.write_queue.pop(0)
                with open(self.directory + item[0] + ".json", "w") as f:
                    json.dump(item[1], f)
            else:
                pass

    def write(self, filename, data):
        self.write_queue.append((filename, data))
