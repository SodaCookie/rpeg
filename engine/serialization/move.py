"""Implements the MoveDataManager class"""
from engine.serialization.dmanager import DataManager
from engine.game.move.move import Move

class MoveDataManager(DataManager):
    """Singleton class used to get and assign move data"""

    def __init__(self):
        super().__init__("data/moves.p")

    def get_move(self, name):
        """Convenience function. To get a move object by name"""
        return self.moves()[name]

    def moves(self):
        """Returns a dictionary to data for moves"""
        return self.get()

    def new_move(self, name):
        move = Move(name)
        self.moves()[name] = move

    def delete_move(self, name):
        del self.moves()[name]

    def update_move_name(self, name, new_name):
        move = self.moves()[name]
        move.name = new_name
        del self.moves()[name]
        self.moves()[new_name] = move

    def update_move_icon(self, name, icon):
        self.moves()[name].icon = icon

    def update_move_animation(self, name):
        return NotImplemented

    def update_move_miss_bound(self, name, miss_bound):
        self.moves()[name].miss_bound = miss_bound

    def update_move_crit_bound(self, name, crit_bound):
        self.moves()[name].crit_bound = crit_bound

    def update_move_description(self, name, desc):
        self.moves()[name].description = desc

    def update_move_statdist(self, name, stype, value):
        self.moves()[name].statdist[stype] = value

    def add_standard_component(self, name, component):
        self.moves()[name].components.append(component)

    def remove_standard_component(self, name, index):
        del self.moves()[name].components[index]

    def add_miss_component(self, name, component):
        self.moves()[name].miss_components.append(component)

    def remove_miss_component(self, name, index):
        del self.moves()[name].miss_components[index]

    def add_crit_component(self, name, component):
        self.moves()[name].crit_components.append(component)

    def remove_crit_component(self, name, index):
        del self.moves()[name].crit_components[index]