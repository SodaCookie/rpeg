import pygame

from engine.ui.core.renderable import Renderable

class PercentBar(Renderable):
    """A Bar takes the output of a draw function and vertically
    or horizontally cuts the rendering based on percentage"""

    def __init__(self, name, x, y, image, horizonal=True):
        super().__init__(name, x, y)
        self.percent = 1.0
        self.horizonal = horizonal
        self.image = image

    def set_percent(self, value):
        self.percent = value

    def render(self, surface, game, system):
        img_width, img_height = self.image.get_size()
        if self.horizonal:
            width = round(img_width * self.percent)
            height = img_height
        else:
            width = img_width
            height = round(img_height * self.percent)

        # Render to the screen
        surface.blit(self.image, (self.x, self.y), (0, 0, width, height))
