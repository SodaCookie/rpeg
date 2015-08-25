class Move(object):

    def __init__(self, name, components = None):
        self.name = name
        self.animation = NotImplemented
        if components != None:
            self.components = components
        else:
            self.components = []

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
        if not any(c.valid_targets(
                selected, caster, players, monsters, targets)
                for c in self.components:
            return None
        #execute the move
        total_msg = ""
        for component in self.components:
            msg = component.on_cast(self, target, caster, players, monsters)
            if msg:
                total_msg += msg + '\n'
        if total_msg.endswith('\n'):
            total_msg = total_msg[:-1]
        return total_msg