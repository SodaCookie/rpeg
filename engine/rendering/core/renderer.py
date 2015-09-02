"""Defines the renderer class"""

class Renderer(object):
    """The Renderer class is responsible for handling the rendering
    of other objects. Therefore, a renderer will not render anything
    itself. Rather is serves as a container for rendering renderables.
    Some renderers may subscribe """
    def __init__(self, renderables=None):
        super(Renderer, self).__init__()
        if renderables == None:
            renderables = []
        self.renderables = renderables

    def render(self, surface, game):
        """Render will take a surface to be passed onto its renderables
        renderer takes the game object to be passed on as it pleases."""
        for r in self.renderables:
            r.render(surface, game)
