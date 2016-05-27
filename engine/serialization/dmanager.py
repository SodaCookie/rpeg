"""Defines the DataManager abstract class"""
import sys

from engine.serialization.serialization import deserialize, serialize

class DataManager(object):
    """In charge of making sure all objects loaded from pickle files
    are not loaded twice into two different objects. This means that
    the loaded objects will share a reference!"""

    # Flyweights
    cache = {}

    def __init__(self, filename):
        if not self.cache.get(filename):
            self.cache[filename] = deserialize(filename)
        self.filename = filename

    def __del__(self):
        """Deletes cached object if no more references"""
        if self.cache.get(self.filename) and \
                sys.getrefcount(self.cache[self.filename]) <= 2:
            del self.cache[self.filename]

    def get(self):
        """Returns the loaded data. None if the filename isn't given"""
        return self.cache.get(self.filename)

    def write(self):
        serialize(self.cache[self.filename], self.filename)