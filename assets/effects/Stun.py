from engine.game.effect.effect import Effect

class Stun(Effect):
    """Sets target's speed to 0 in order to stun"""

    def __init__(self, duration):
        """Prevents action from building.
        duration -> float"""
        super().__init__("stunned", duration)

    def on_build_action(self, action):
        return 0
