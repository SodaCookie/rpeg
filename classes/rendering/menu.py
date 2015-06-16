from classes.rendering.view import Renderable

class Menu(Renderable):
    """docstring for Menu"""
    BREAK = 0 # returning BREAK will halt all drawing

    def __init__(self, name, pos, game, render_info):
        super(Menu, self).__init__(pos)
        self.name = name
        self.game = game
        self.render_info = render_info
        self.rendering = []

    def add(self, renderable):
        renderable.master = self
        renderable.show()
        self.rendering.append(renderable)
        return renderable

    def remove(self, renderable):
        renderable.master = None
        self.rendering.remove(renderable)

    def hide(self):
        super().hide()
        for r in self.rendering:
            r.hide()

    def show(self):
        super().show()
        for r in self.rendering:
            r.show()

    def clear(self):
        """Just delete everything that belongs to it"""
        for r in self.rendering:
            r.delete()
        self.rendering = []

    def delete(self):
        """Delete itself and everything that belongs to it"""
        super().delete()
        for r in self.rendering:
            r.delete()
        self.rendering = []

    def draw(self, screen):
        if self.draw_before(screen) == Menu.BREAK:
            return

        if not self.visible:
            return

        for r in self.rendering:
            r.draw(screen)

    def draw_before(self, screen):
        """Override this function to change how things will be rendered"""
        pass