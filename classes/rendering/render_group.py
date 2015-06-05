from classes.rendering.view import Renderable
from classes.image_cache import ImageCache

class RenderGroup(Renderable):
    """docstring for RenderGroup"""
    def __init__(self, name, pos=(0, 0)):
        super().__init__(pos)
        self.name = name
        self.displaying = False
        self.rendering = []
        self.pos = pos

    def add(self, renderable):
        if renderable not in self.rendering:
            pos = renderable.pos
            renderable.move((self.pos[0]+pos[0], self.pos[1]+pos[1]))
            self.rendering.append(renderable)

    def remove(self, renderable):
        if isinstance(renderable, RenderGroup):
            delattr(self, renderable.name)

        if renderable in self.rendering:
            pos = renderable.pos
            renderable.move((self.pos[0]-pos[0], self.pos[1]-pos[1]))
            self.rendering.remove(renderable)

    def render(self):
        pass

    def display(self):
        if self.displaying:
            return
        self.displaying = True
        for r in self.rendering:
            r.display()

    def update(self):
        self.delete()
        self.render()
        self.display()

    def delete(self):
        if not self.displaying:
            return
        self.displaying = False
        for r in self.rendering:
            r.delete()
        self.rendering = []
