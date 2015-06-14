from classes.rendering.view import Renderable

class Menu(Renderable):
    """docstring for Menu"""
    BREAK = 0 # returning BREAK will halt all drawing

    def __init__(self, name, pos, game, render_info):
        super(Menu, self).__init__(pos)
        self.game = game
        self.render_info = render_info
        self.rendering = []

    def add(self, renderable):
        renderable.master = self
        self.rendering.append(renderable)
        return renderable

    def remove(self, renderable):
        renderable.master = None
        self.rendering.remove(renderable)

    def draw(self, screen):
        if self.draw_before(screen) == Menu.BREAK:
            return
        for r in self.rendering:
            r.draw(screen)

    def draw_before(self, screen):
        """Override this function to change how things will be rendered"""
        pass