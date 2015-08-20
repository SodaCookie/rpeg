from classes.rendering.render_group import RenderGroup

class Bars(RenderGroup):

    def __init__(self):
        super().__init__("bars")
        self.bars = []

    def add(self, bars):
        self.bars.append(bars)

    def remove(self, bars):
        self.bars.remove(bars)

    def update(self):
        for group in self.bars:
            group.update()