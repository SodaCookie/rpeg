"""Defines the manager class"""
import logging

from collections import OrderedDict

from engine.ui.core.renderable import Renderable

class Manager(Renderable):
    """The Manager class is responsible for handling the rendering
    of renderable objects and the updating of zones. It defines
    update and render methods and renderables and zones as attributes."""

    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.renderables = OrderedDict()

    def add_renderable(self, renderable):
        """Add a renderable to the running list of renderables"""
        if not self.renderables.get(renderable.name):
            self.renderables[renderable.name] = renderable
        else:
            logging.error("Renderable with the same name has been added to %s"\
                % self.name)

    def get_renderable(self, name):
        return self.renderables[name]

    def remove_renderable(self, name):
        """Remove the renderable from the maintained group of renderables"""
        del self.renderables[name]

    def clear(self):
        """Deletes every Renderable"""
        self.renderables = OrderedDict()

    def update(self, game, system):
        """Override. Called before rendering"""
        pass

    def render(self, surface, game, system):
        """Render will take a surface to be passed onto its renderables
        renderer takes the game object to be passed on as it pleases."""
        self.update(game, system)
        for r in self.renderables.values():
            r.render(surface, game, system)
