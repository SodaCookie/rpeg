from engine.game.move.component import Component
from assets.moves.components.TargetNumberOnly import TargetNumberOnly

class TargetOneOnly(TargetNumberOnly):
    """Descriptor for targeting one character only"""

    def __init__(self):
        super().__init__(1)