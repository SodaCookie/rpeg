import random

import pygame

import classes.game.effect as effect


class MoveBase(object):
    """Base class of all moves, implements almost nothing
    a critical roll will propagate all the way down the move list
    a miss roll will propagate all the way down the move list.
    All classes extending this class should have name as their last
    parameter and contain no **kwargs or *args"""

    def __init__(self, name):

        if type(name) == str:
            self.name = name
            self.prev = None
            self.targetting = None # an optional identifier for targeting type
        elif issubclass(type(name), MoveBase):
            self.name = name.name
            self.prev = name

        self.targeting = "none"
        self.caster = None
        self.accuracy = 100
        self.critical = 0
        self.target = None
        self.surface = None

        self.cur_accuracy = self.accuracy
        self.cur_crit = self.critical

    def set_caster(self, caster):
        self.caster = caster
        if self.prev:
            self.prev.set_caster(caster)

    def set_crit(self, crit):
        self.cur_crit = crit

    def get_crit(self):
        return self.cur_crit

    def get_accuracy(self):
        return self.cur_accuracy

    def set_accuracy(self, accuracy):
        self.cur_accuracy = accuracy

    def get_target(self, battle):
        """Targeting function is taken via the most inner function"""
        return []

    def run(self, battle):
        if random.randint(0, 99) <= self.cur_accuracy:  # accuracy roll
            if random.randint(0, 99) < self.cur_crit:  # crit roll
                self._crit(battle)
            else:
                self._cast(battle)
        else:
            self._miss(battle)

        # reset the accuracy and crit after cast
        self.cur_accuracy = self.accuracy
        self.cur_crit = self.critical

    def _cast(self, battle):
        self.target = self.get_target(battle)

        if self.prev:
            self.prev._cast(battle)

        for target in self.target:
            self.cast(target)

    def _crit(self, battle):
        self.target = self.get_target(battle)

        if self.prev:
            self.prev._crit(battle)

        for target in self.target:
            self.crit(target)

    def _miss(self, battle):
        self.target = self.get_target(battle)

        if self.prev:
            self.prev._miss(battle)

        for target in self.target:
            self.miss(target)

    def crit(self, target):
        """Override when wanting to make crit effect"""
        pass

    def miss(self, target):
        """Override when want to make a miss effect"""
        pass

    def cast(self, target):
        """Override to create effects"""
        pass


class Move(MoveBase):
    """Wrapper class that added critical chance and accuracy,
    implements a basic get_target method and crit method"""

    def __init__(self, accuracy, crit, surface, targeting, name):
        super().__init__(name)

        self.targeting = targeting
        self.accuracy = accuracy
        self.crit = crit
        self.surface = surface
        self.target = None

        self.cur_accuracy = self.accuracy
        self.cur_crit = self.crit

    def crit(self):
        """Override when wanting to make crit effect"""
        self.cast()

if __name__ == "__main__":
    # Testing
    nmove = Move("test")