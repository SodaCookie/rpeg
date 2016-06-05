import pygame

from engine.ui.core.renderable import Renderable

class PercentBar(Renderable):
    """A Bar takes the output of a draw function and vertically
    or horizontally cuts the rendering based on percentage"""

    def __init__(self, name, x, y, image, horizonal=True):
        super().__init__(name, x, y)
        self.percent = 100
        self.horizonal = horizonal
        self.image = image

    def render(self, surface, game, system):
        img_width, img_height = self.image.size()
        if self.horizonal:
            width = round(self.width * self.percent / 100)
            height = self.height
        else:
            width = self.width
            self.height = round(self.height * self.percent / 100)

        # Render to the screen
        surface.blit(self.image, (self.x, self.y), (0, 0, width, height))
