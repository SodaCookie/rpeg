import random
import objects.effect as effect

class Move(object):

    def __init__(self, name, **kwargs):

        if type(name) == str:
            self.name = name
            self.prev = None
        elif issubclass(type(name), Move):
            self.name = name.name
            self.prev = name

        self.caster = None
        self.accuracy = 100
        self.crit = 0
        self.target = None
        for key in kwargs.keys():
            if key == "accuracy":
                self.accuracy = kwargs[key]
            elif key == "crit":
                self.crit = kwargs[key]
        self.cur_accuracy = self.accuracy
        self.cur_crit = self.crit

    def set_caster(self, caster):
        self.caster = caster
        if self.prev:
            self.prev.set_caster(caster)

    def set_crit(self, crit):
        self.cur_crit = crit

    def get_crit(self):
        return self.cur_crit

    def get_accuracy(self):
        return   self.cur_accuracy

    def set_accuracy(self, accuracy):
        self.cur_accuracy = accuracy

    def cast(self, battle):
        self.target = self.get_target(battle)

        if self.prev:
            self.prev.cast()

        if random.randint(0, 99) <= self.cur_accuracy:  # accuracy roll
            if isinstance(self.target(), list):
                for member in self.target:
                    if random.randint(0, 99) < self.cur_crit:  # crit roll
                        self._crit()
                    else:
                        self._cast()
            else:
                if random.randint(0, 99) < self.cur_crit:  # crit roll
                    self._crit()
                else:
                    self._cast()
        else:
            self._miss()

        # reset the accuracy and crit after cast
        self.cur_accuracy = self.accuracy
        self.cur_crit = self.crit

    def get_target(self, battle):
        return None

    def _crit(self):
        """Override when wanting to make crit effect"""
        self._cast()

    def _miss(self):
        """Override when want to make a miss effect"""
        pass

    def _cast(self):
        """Override to create effects"""
        pass


if __name__ == "__main__":
    # Testing
    nmove = Move("test")