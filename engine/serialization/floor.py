"""Implements the FloorDataManager class"""
from engine.serialization.dmanager import DataManager

class FloorDataManager(DataManager):
    """Singleton class used to get and assign floor data"""

    def __init__(self):
        super().__init__("data/floors.p")

    def floors(self):
        return self.get()

    def add_floor(self, floorname):
        """Adds a floor type to the floors list"""
        floor = self.get()
        floot.append(floorname)

    def remove_floor(self, floorname):
        """Remvoes a floor type to the floors list"""
        floor = self.get()
        floor.remove(floorname)