import os
import json
import threading
import random
import time

class ListenerBase:
    def __init__(self, directory):
        self.directory = directory
        try:
            os.makedirs(self.directory)
        except FileExistsError:
            pass
        self.thread = threading.Thread(target=self.listen)
        self.thread.start()
        self.queue = []

    def listen(self):
        while True:
            time.sleep(0.1)
            try:
                dir = os.listdir(self.directory)
                self.queue = [i.split(".")[0] for i in dir]
            except FileNotFoundError:
                pass

    def get_queue_item(self, id, no_delete = False):
        try:
            item = self.queue[self.queue.index(id)]
            with open(self.directory + item + ".json", "r") as f:
                if f.readable():
                    data = json.load(f)
            try:
                if not no_delete:
                    os.remove(self.directory + item + ".json")
            except:
                pass
            return data
        except FileNotFoundError:
            return None
        finally:
            try:
                if not no_delete:
                    self.queue.remove(id)
            except:
                pass

    def get_random_item(self, no_delete = False):
        _ = random.choice(self.queue)
        return self.get_queue_item(_, no_delete), _

    def delete(self, id):
        try:
            os.remove(self.directory + id + ".json")
            self.queue.remove(id)
        except:
            pass

    def get_first_item(self, no_delete = False):
        return self.get_queue_item(self.queue[0], no_delete)

    def get_last_item(self, no_delete = False):
        return self.get_queue_item(self.queue[-1], no_delete)

    def remove_first_item(self):
        try:
            os.remove(self.directory + self.queue[0] + ".json")
            self.queue.remove(self.queue[0])
        except:
            pass

    def get_queue_length(self):
        return len(self.queue)

    def wait_read(self, id):
        while True:
            try:
                ret = self.get_queue_item(id)
                return ret
            except:
                pass

class WriterBase:
    def __init__(self, directory):
        self.directory = directory
        self.written = 0
        try:
            os.mkdir(self.directory)
        except FileExistsError:
            pass

    def write(self, filename, data):
        if not filename == "CUSTOM":
            if filename == "AUTO":
                filename = str(self.written + 1)
                while True:
                    if os.path.exists(self.directory + filename + ".json"):
                        filename = str(self.written + 1)
                        self.written += 1
                        break
            with open(self.directory + filename + ".json", "w") as f:
                dat = json.dumps(data)
                f.write(dat)
            self.written += 1
        else:
            with open(self.directory + filename + ".json", "w") as f:
                dat = json.dumps(data)
                f.write(dat)
            self.written += 1
