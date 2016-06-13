"""Defines the Renderable abstract base class"""

class Renderable(object):
    """Renderable is an abstract base class that simply defines a
    render method for subclasses to implement. As of right now I'm
    experimenting with the idea of having minimal overhead of this
    base class so render will not be expected to return anything."""

    def __init__(self, name, x, y):
        """Renderable takes no arguments as I want to limit
        the overhead of this abstract class for this iteration."""
        super().__init__()
        self.name = name
        self.x = x
        self.y = y

    def message(self, game, system, message):
        """Override. Called when message is passed"""
        pass

    def render(self, surface, game, system):
        """Render is given a surface of which to draw on. Game object
        for when the object has to draw according to the game."""
        pass

    def move(self, x, y):
        """Moves the renderable location absolutely"""
        self.x = x
        self.y = y