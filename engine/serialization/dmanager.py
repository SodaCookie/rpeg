"""Defines the DataManager abstract class"""
import sys

from engine.serialization.serialization import deserialize, serialize

class DataManager(object):
    """In charge of making sure all objects loaded from pickle files
    are not loaded twice into two different objects. This means that
    the loaded objects will share a reference!"""

    # Flyweights
    cache = {}
    # Use our own reference counting system
    refcounts = {}

    def __init__(self, filename):
        if not DataManager.cache.get(filename):
            DataManager.cache[filename] = deserialize(filename)
        if filename in DataManager.refcounts:
            DataManager.refcounts[filename] += 1
        else:
            DataManager.refcounts[filename] = 1
        self.filename = filename

    def __del__(self):
        """Deletes cached object if no more references"""
        DataManager.refcounts[self.filename] -= 1
        if DataManager.refcounts[self.filename] <= 0:
            del DataManager.cache[self.filename]
            del DataManager.refcounts[self.filename]

    def get(self):
        """Returns the loaded data. None if the filename isn't given"""
        return DataManager.cache[self.filename]

    def set(self, value):
        DataManager.cache[self.filename] = value

    def write(self):
        serialize(DataManager.cache[self.filename], self.filename)

    @classmethod
    def writeall(self):
        """Saves all the cached functions at once."""
        for file, data in DataManager.cache.items():
            serialize(data, file)