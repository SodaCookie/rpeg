from image_cache import ImageCache
from view import Renderable

class Image(Renderable):
    def __init__(self, pos, h_anchor=0, v_anchor=0, surface=None, filename="", alpha=False):
        super().__init__(pos)

        if filename != "":
            self.img = ImageCache.add(filename, alpha)
        else:
            self.img = surface
        self.h_anchor = h_anchor
        self.v_anchor = v_anchor

    def delete(self):
        super().delete()

    def draw(surface):
        size = self.img.get_size()

        if self.h_anchor < 0:
            x_offset = -size[0]
        elif self.h_anchor > 0:
            x_offset = 0
        else:
            x_offset = -size[0] / 2

        if self.v_anchor < 0:
            y_offset = -size[1]
        elif self.v_anchor > 0:
            y_offset = 0
        else:
            y_offset = -size[1] / 2

        surface.blit(self.img, (self.pos[0] + x_offset, self.pos[1] + y_offset))