# imports
import gzip
import json
import os
import random
import threading
import time

# external imports
from settings import *


class ListenerBase:
    """
    ListenerBase

    This class is used to listen to a directory and get the files in it.
    Uses gzip to inflate the json files, which were compressed with WriteBase.
    BTW, pcdt stands for 'PyCraft Data Transfer'
    """

    def __init__(self, directory):
        """
        Initialize the ListenerBase class.

        :param directory: The directory to listen to.
        """
        self.directory = directory
        try:
            # create the directory if it doesn't exist
            os.makedirs(self.directory)
        except FileExistsError:
            pass
        self.thread = threading.Thread(
            target=self.listen)  # create a 'listen' thread
        self.thread.start()  # start the thread
        self.queue = []  # initialize the queue list

    def listen(self):
        """
        Listen to the directory and add the files to the queue.
        """
        while True:
            try:
                dir = os.listdir(self.directory)  # list the directory
                self.queue = [i.split(".")[0]
                              for i in dir]  # add the files to the queue
            except FileNotFoundError:  # if the directory doesn't exist
                pass  # do nothing

    def get_queue_item(self, id, no_delete=False):
        """
        Get an item from the queue.

        :param id: The id of the item.
        :param no_delete: If the item should be deleted from the directory.

        :return: The item's data, decoded using Base64.
        """
        try:
            # get the item from the queue
            item = self.queue[self.queue.index(id)]
            with open(self.directory + item + ".pcdt", "rb") as f:  # open the file
                if f.readable():  # if the file is readable, i.e. not being written to
                    data = gzip.decompress(f.read()).decode("utf-8") # read the file
                    data = json.loads(data)  # load the json data
            try:
                if not no_delete:  # if the item should be deleted
                    os.remove(self.directory + item +
                              ".pcdt")  # delete the file
            except:  # if the file doesn't exist
                pass  # do nothing
            return data  # return the data
        except FileNotFoundError:  # if the file doesn't exist
            return None  # return nothing
        finally:
            try:
                if not no_delete:  # if the item should be deleted
                    self.queue.remove(id)  # remove the item from the queue
            except:  # if the item doesn't exist
                pass  # do nothing

    def get_random_item(self, no_delete=False):
        """
        Get a random item from the queue.

        :param no_delete: If the item should be deleted from the directory.

        :return: A list with the item's data and id.
        """
        _ = random.choice(self.queue)  # get a random item from the queue
        # return the item's data and id
        return self.get_queue_item(_, no_delete), _

    def delete(self, id):
        """
        Delete an item from the queue.

        :param id: The id of the item.
        """
        try:
            os.remove(self.directory + id + ".pcdt")  # delete the file
            self.queue.remove(id)  # remove the item from the queue
        except:  # if the file doesn't exist
            pass  # do nothing

    def get_first_item(self, no_delete=False):
        """
        Get the first item from the queue.

        :param no_delete: If the item should be deleted from the directory.

        :return: The item's data, decoded using Base64.
        """
        return self.get_queue_item(self.queue[0], no_delete)

    def get_last_item(self, no_delete=False):
        """
        Get the last item from the queue.

        :param no_delete: If the item should be deleted from the directory.

        :return: The item's data, decoded using Base64.
        """
        return self.get_queue_item(self.queue[-1], no_delete)

    def remove_first_item(self):
        """
        Remove the first item from the queue.
        """
        try:
            # delete the file
            os.remove(self.directory + self.queue[0] + ".pcdt")
            self.queue.remove(self.queue[0])  # remove the item from the queue
        except:  # if the file doesn't exist
            pass  # do nothing

    def get_queue_length(self):
        """
        Get the length of the queue.

        :return: The length of the queue.
        """
        return len(self.queue)

    def wait_read(self, id):
        """
        Wait for an item to be readable, then return it.

        :param id: The id of the item.

        :return: The item's data, decoded using Base64.
        """
        while True:
            try:
                ret = self.get_queue_item(id)  # get the item
                return ret  # return the item
            except:  # if the item doesn't exist
                pass  # do nothing


class WriterBase:
    """
    WriterBase

    This class is used to write json to a directory.

    BTW, pcdt stands for 'PyCraft Data Transfer'
    """

    def __init__(self, directory):
        """
        Initialize the WriterBase class.

        :param directory: The directory to write to.
        """
        self.directory = directory  # set the directory
        self.written = 0  # initialize the written counter
        try:
            # create the directory if it doesn't exist
            os.mkdir(self.directory)
        except FileExistsError:  # if the directory already exists
            pass  # do nothing

    def write(self, filename, data):
        """
        Write data to a file.

        :param filename: The filename to write to.
        :param data: The data to write.

        :return: The filename.
        """
        if not filename == "CUSTOM":  # if the filename is not custom
            if filename == "AUTO":  # if the filename is auto
                # set the filename to the written counter
                filename = str(self.written + 1)
                while True:  # loop until the filename is unique
                    # if the file exists
                    if os.path.exists(self.directory + filename + ".pcdt"):
                        # set the filename to the written counter
                        filename = str(self.written + 1)
                        self.written += 1  # increment the written counter
                    else:  # if the file doesn't exist
                        break  # break the loop
            with open(self.directory + filename + ".pcdt", "wb") as f:  # open the file
                data = json.dumps(data)  # dump the data to json
                # encode the data using Base64
                data = gzip.compress(data.encode("utf-8"))
                f.write(data)  # write the data to the file
                del data  # delete the data to free up memory
            self.written += 1  # increment the written counter
        else:  # if the filename is custom
            with open(self.directory + filename + ".pcdt", "wb") as f:  # open the file
                data = json.dumps(data)  # dump the data to json
                # encode the data using Base64
                data = gzip.compress(data.encode("utf-8"))
                f.write(data)  # write the data to the file
                del data  # delete the data to free up memory
            self.written += 1  # increment the written counter

        return filename  # return the filename
