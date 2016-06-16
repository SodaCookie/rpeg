"""Implements the FloorDataManager class"""
from engine.serialization.dmanager import DataManager

class FloorDataManager(object):
    """Singleton class used to get and assign floor data"""

    # NOTE: data currently stored as a list of floor names
    # Potentially better to do a set of floor names?

    def __init__(self):
        self.FLOORS = DataManager("data/floors.p")

    def floors(self):
        return self.FLOORS.get()

    def add_floor(self, floorname):
        """Adds a floor type to the floors list"""
        floor = self.FLOORS.get()
        floor.append(floorname)

    def remove_floor(self, floorname):
        """Removes a floor type to the floors list"""
        floor = self.FLOORS.get()
        floor.remove(floorname)

    def write(self):
        self.FLOORS.write()

    def set(self, floors):
        self.FLOORS.set(floors)

