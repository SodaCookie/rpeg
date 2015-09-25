class Move(object):

    def __init__(self, name, icon=None, components=None, miss_bound=0,
                 miss_comp=None, crit_bound=100, crit_comp=None):
        self.name = name
        self.caster = None
        self.icon = icon
        self.animation = NotImplemented
        # Standard Move
        if components != None:
            self.components = components
        else:
            self.components = []
        self.miss_bound = miss_bound
        # Miss Move
        if miss_comp != None:
            self.miss_comp = miss_comp
        else:
            self.miss_comp = []
        # Critical Move
        if crit_comp != None:
            self.crit_comp = crit_comp
        else:
            self.crit_comp = []

        self.miss_bound = miss_bound
        self.crit_bound = crit_bound

    def set_caster(self, caster):
        self.caster = caster

    def cast(self, selected, caster, players, monsters):
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
                targets = component_targets
        assert targets, "Move must have a target"
        # Validates targets
        if not any(c.valid_targets(selected, self.caster, players, monsters, targets) for c in self.components):
            return None
        #execute the move
        total_msg = ""
        for target in targets:
            for component in self.components:
                msg = component.on_cast(target, caster, players, monsters)
                if msg:
                    total_msg += msg + '\n'
        if total_msg.endswith('\n'):
            total_msg = total_msg[:-1]
        return total_msg

