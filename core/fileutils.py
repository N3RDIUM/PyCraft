import os
import json
import threading
import sys
import glfw

def print_from_process(string):
    print(string)
    sys.stdout.flush()

class ListenerBase:
    def __init__(self, directory, window):
        self.directory = directory
        self.window = window
        self.process = threading.Thread(target=self.listen)
        self.process.start()
        self.queue = []

    def listen(self):
        while glfw.window_should_close(self.window) == 0:
            try:
                dir = os.listdir(self.directory)
                self.queue = [i.split(".")[0] for i in dir]
            except FileNotFoundError:
                os.mkdir(self.directory)

        os.rmdir(self.directory)

    def get_queue_item(self, id):
        item = self.queue.pop(id)
        with open(self.directory + item + ".json", "r") as f:
            data = json.load(f)
        os.remove(self.directory + item + ".json")
        return data

    def get_queue_length(self):
        return len(self.queue)

class WriterBase:
    def __init__(self, directory):
        self.directory = directory
        self.written = 0

    def write(self, filename, data):
        if filename == "AUTO":
            filename = str(self.written + 1)
        with open(self.directory + filename + ".json", "w") as f:
            json.dump(data, f)
        self.written += 1
