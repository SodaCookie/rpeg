class Effect:

    PERMANENT = "permanent" # Given to permanent Effects
                            # can be removed with remove()

    def __init__(self, name, duration, tick=None):
        """ Effects are actions that trigger after a certain action is made
        'name' is the identifier used to identify the effect
        duration is used to indicate how long the effect will last on the
        target. Durations for each effect on a target are decreased by 1
        after that character's turn
        """
        self.name = name
        self.max_duration = duration
        self.duration = duration
        self.tick = tick
        if not tick:
            self.cur_tick = 0
        else:
            self.cur_tick = self.max_duration - tick
        self.active = True
        self.owner = None
        self.caster = None

    def set_owner(self, owner):
        self.owner = owner

    def set_caster(self, caster):
        self.caster = caster

    def remove(self):
        """Inactivates and removes effect
        When called any subsequent calls to this effect will be ignored as
        well as removed useful for 1 time effects
        """
        self.duration = 0
        self.active = False

    def on_remove(self):
        pass

    def on_refresh(self, effect):
        self.duration = self.max_duration

    def on_tick(self):
        pass

    def on_deal_damage(self, damage, damage_type):
        """Returns the amount of modified damage the target receives
        When host deals an amount of damage
        """
        return damage

    def on_get_stat(self, value, stat_type):
        """Returns the modified stat value
        Any time a character is asked for a stat this function will be
        called and the type of stat will be used to determine how the stat
        will be affected. Returned is the stat of the player
        """
        return value

    def on_start_turn(self):
        pass

    def on_build_action(self, action):
        """Each time the character wants to build action value"""
        return action

    def on_damage(self, source, damage, damage_type):
        return damage

    def on_heal(self, source, heal):
        return heal

    def on_apply_heal(self, heal):
        return heal

    def on_cast(self, source, move):
        pass

    def on_death(self):
        """If truly dead then return True"""
        return True

    def on_move(self, location):
        pass

    def __str__(self):
        return "%s - Turn(s)%d" % (self.name.replace("-", " ").title(),
                                   self.duration)