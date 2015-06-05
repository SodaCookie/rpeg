from classes.rendering.view import Renderable
from classes.rendering.image_cache import ImageCache

class RenderGroup(Renderable):
    """docstring for RenderGroup"""
    def __init__(self, name, pos=(0, 0)):
        super().__init__()
        self.name = name
        self.renderables
        self.pos = pos

    def add(self, renderable):
        if isinstance(renderable, RenderGroup):
            setattr(self, renderable.name, renderable)

        if renderable not in self.renderables:
            pos = renderable.pos
            renderable.move((self.pos[0]+pos[0], self.pos[1]+pos[1]))
            self.renderables.append(renderable)

    def remove(self, renderable):
        if isinstance(renderable, RenderGroup):
            delattr(self, renderable.name)

        if renderable in self.renderables:
            pos = renderable.pos
            renderable.move((self.pos[0]-pos[0], self.pos[1]-pos[1]))
            self.renderables.remove(renderable)

    def render(self):
        pass

    def display(self):
        for r in self.renderables:
            r.display()

    def update(self):
        self.delete()
        self.display()

    def delete(self):
        for r in self.renderables:
            r.delete()
