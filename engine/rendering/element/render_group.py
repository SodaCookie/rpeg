from classes.rendering.view import Renderable
from classes.image_cache import ImageCache

class RenderGroup(Renderable):

    # theres a bug where pos is set but render is called before

    def __init__(self, name, pos=(0, 0)):
        super().__init__(pos)
        self.name = name
        self.displaying = False
        self.rendering = []
        self.pos = pos

    def add(self, renderable):
        if isinstance(renderable, RenderGroup):
            for r in renderable.rendering:
                pos = r.pos
                r.move((self.pos[0]+pos[0], self.pos[1]+pos[1]))
            pos = renderable.pos
            renderable.move((self.pos[0]+pos[0], self.pos[1]+pos[1]))
            self.rendering.append(renderable)
        else:
            pos = renderable.pos
            renderable.move((self.pos[0]+pos[0], self.pos[1]+pos[1]))
            self.rendering.append(renderable)

    def remove(self, renderable):
        pos = renderable.pos
        renderable.move((self.pos[0]-pos[0], self.pos[1]-pos[1]))
        self.rendering.remove(renderable)

    def hide(self):
        self.displaying = False
        self.visible = False
        for r in self.rendering:
            r.hide()

    def render(self):
        pass

    def display(self):
        if self.displaying:
            return
        self.visible = True
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
        self.visible = False
        for r in self.rendering:
            r.delete()
        self.rendering = []
