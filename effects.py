class Effect:

    def __init__(self, name, duration):
        """'name' is the identifier used to identify the effect
        duration is used to indicate how long the effect will last on the target.
        Durations for each effect on a target are decreased by 1 after that
         character's turn"""
        self.name = name
        self.duration = duration
        self.active = True

    def remove(self):
        """When called any subsequent calls to this effect will be ignored as well as removed
        useful for 1 time effects"""
        self.duration = 0
        self.active = False

    def on_get_stat(self, value, stat_type):
        """Any time a character is asked for a stat this function will be called
        and the type of stat will be used to determine how the stat will be
        affected. Returned is the stat of the player"""
        return value

    def on_start_turn(self, character):
        """Return a tuple index 0 true if you can go, return false if you can't (ie stun, dead), index 1 is the message"""
        pass

    def on_damage(self, source, damage, damage_type):
        return damage

    def on_heal(self, source, heal):
        return heal

    def on_cast(self, source, move):
        pass

    def on_death(self, character):
        """If truly dead then return True"""
        return True

    def on_end_turn(self, character):
        """That is the end of the characters turn (not the WHOLE turn), returns message"""
        pass

    def __str__(self):
        return "%s - Turn(s)%d" % (self.name.replace("-", " ").title(), self.duration)