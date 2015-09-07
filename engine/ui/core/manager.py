"""Defines the manager class"""

class Manager(object):
    """The Manager class is responsible for handling the rendering
    of renderable objects and the updating of zones. It defines
    update and render methods and renderables and zones as attributes."""

    def __init__(self):
        self.renderables = []
        self.zones = []

    def update(self, game):
        """Updates the zones in the game"""
        for z in self.zones:
            z.update(game)

    def render(self, surface, game):
        """Render will take a surface to be passed onto its renderables
        renderer takes the game object to be passed on as it pleases."""
        for r in self.renderables:
            r.render(surface, game)
