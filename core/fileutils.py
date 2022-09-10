import os
import json
import threading

class ListenerBase:
    def __init__(self, directory):
        self.directory = directory
        try:
            os.mkdir(self.directory)
        except FileExistsError:
            pass
        self.process = threading.Thread(target=self.listen)
        self.process.start()
        self.queue = []

    def listen(self):
        while True:
            try:
                dir = os.listdir(self.directory)
                self.queue = [i.split(".")[0] for i in dir]
            except FileNotFoundError:
                pass

    def get_queue_item(self, id):
        try:
            item = self.queue[self.queue.index(id)]
            with open(self.directory + item + ".json", "r") as f:
                while True:
                    try:
                        data = json.load(f)
                        break
                    except json.decoder.JSONDecodeError:
                        pass
            try:
                os.remove(self.directory + item + ".json")
            except:
                pass
            return data
        except FileNotFoundError:
            return None
        finally:
            try:
                self.queue.remove(id)
            except:
                pass

    def get_first_item(self):
        return self.get_queue_item(self.queue[0])

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
            with open(self.directory + filename + ".json", "w") as f:
                json.dump(data, f)
            self.written += 1
        else:
            filename = str(self.written + 1)
            with open(self.directory + filename + ".json", "w") as f:
                f.write(data)
            self.written += 1
