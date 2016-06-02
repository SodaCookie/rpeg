"""Defines the Renderable abstract base class"""

class Renderable(object):
    """Renderable is an abstract base class that simply defines a
    render method for subclasses to implement. As of right now I'm
    experimenting with the idea of having minimal overhead of this
    base class so render will not be expected to return anything."""

    def __init__(self, name):
        """Renderable takes no arguments as I want to limit
        the overhead of this abstract class for this iteration."""
        super().__init__()
        self.name = name

    def render(self, surface, game, system):
        """Render is given a surface of which to draw on. Game object
        for when the object has to draw according to the game."""
        pass