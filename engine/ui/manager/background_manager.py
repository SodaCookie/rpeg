from engine.ui.core.manager import Manager

import engine.ui.element as element
from engine.ui.draw.simple import draw_image

class BackgroundManager(Manager):

    def __init__(self, start_img):
        super().__init__("background", 0, 0)
        self.img_element = element.Image("image", self.x, self.y,
            draw_image(start_img))
        self.add_renderable(self.img_element)

    def set_image(self, image):
        self.img_element.set_surface(image)

    def get_image(self):
        return self.img_element.surface

    def message(self, game, system, message):
        if message.mtype == "change":
            image = message.args[0]
            self.set_image(image)