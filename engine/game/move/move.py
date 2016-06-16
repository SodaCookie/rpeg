import random

class Move(object):
    """Contains a character's move's definition and how it interacts
    with characters in battle"""

    def __init__(self, name, icon=None, description="", statdist=None,
                 components=None, miss_bound=0, miss_components=None,
                 crit_bound=100, crit_components=None):
        self.name = name
        self.caster = None
        self.icon = icon
        self.animation = NotImplemented
        self.description = description
        self.statdist = {
            'attack': 0,
            'defense': 0,
            'magic': 0,
            'resist': 0,
            'speed': 0,
            'health': 0,
            'action': 0
        }
        if statdist:
            self.statdist.update(statdist)

        # Standard Move
        if components != None:
            self.components = components
        else:
            self.components = []
        self.miss_bound = miss_bound
        # Miss Move
        if miss_components != None:
            self.miss_components = miss_components
        else:
            self.miss_components = []
        # Critical Move
        if crit_components != None:
            self.crit_components = crit_components
        else:
            self.crit_components = []

        self.miss_bound = miss_bound
        self.crit_bound = crit_bound

    def is_valid_target(self, selected, players, monsters):
        return all(c.valid_target(selected, self.caster, players,
            monsters) for c in self.components)

    def is_valid_cast(self, selected, players, monsters):
        return all(c.valid_cast(selected, self.caster, players,
            monsters) for c in self.components)

    def set_caster(self, caster):
        self.caster = caster

    def cast(self, selected, caster, players, monsters, system):
        """Casting the move
        Rule for targets, if targets return empty list than it is
        ignored if list is added If two are given the component that is
        added last will be the list. None is returned if the cast is invalid
        If valid will return a message saying what transpired"""
        # Find targets
        targets = []
        for component in self.components:
            component_targets = component.get_targets(
                selected, caster, players, monsters)
            if component_targets:
                targets.extend(component_targets)
        assert targets, "Move must have a target"

        # roll for the miss, normal or crit
        miss_bound = self.miss_bound
        crit_bound = self.crit_bound
        for component in self.components:
            miss_bound = component.get_miss(miss_bound, selected,
                caster, players, monsters)
            crit_bound = component.get_crit(crit_bound, selected,
                caster, players, monsters)
        roll = random.randint(0, 99)
        if roll < miss_bound:
            move = self.miss_components
        elif miss_bound <= roll < crit_bound:
            move = self.components
        else:
            move = self.crit_components

        # execute the move
        total_msg = ""
        for target in targets:
            for component in move:
                msg = component.on_cast(target, caster, players, monsters,
                    system)
                if msg:
                    total_msg += msg + '\n'
        if total_msg.endswith('\n'):
            total_msg = total_msg[:-1]
        return total_msg

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self