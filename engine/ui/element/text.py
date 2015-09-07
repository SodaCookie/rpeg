import pygame

from engine.ui.core.renderable import Renderable

class Text(Renderable):

    font_cache = {}
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"

    def __init__(self, text, size, x, y,
                 colour=pygame.Color("white"), width=None, justify=LEFT):
        super().__init__()
        self.text = text
        self.size = size
        self.x = x
        self.y = y
        self.colour = colour
        self.width = width
        self.justify = justify
        self.surface = self.draw(self.text, self.size, self.colour,
                                 self.width, self.justify)

    @classmethod
    def draw(self, text, size, colour, width, justify):
        if not Text.font_cache.get(size):
            with open("fonts/VT323-Regular.ttf", 'r') as file:
                Text.font_cache[size] = pygame.font.Font(
                    "fonts/VT323-Regular.ttf", size)
        # text wrapping
        if width:
            lines = []
            for paragraph in map(
                    lambda line: Text._word_wrap(line[0], width, \
                    Text.font_cache[size]), zip(text.split('\n'))):
                lines.extend(paragraph)
                lines.append('')
            lines = lines[:-1] # remove the last return
            height = sum(Text.font_cache[size].size(line)[1] for line in lines)
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            surface.fill((0, 0, 0, 0))

            # drawing the line
            line_height = 0
            for line in lines:
                tmp_line_surf = Text.font_cache[size].render(line, 1, colour)
                if justify == Text.LEFT:
                    surface.blit(tmp_line_surf, (0, line_height))
                elif justify == Text.RIGHT:
                    surface.blit(tmp_line_surf,
                        (width-tmp_line_surf.get_width(), line_height))
                elif justify == Text.CENTER:
                    surface.blit(tmp_line_surf,
                        ((width-tmp_line_surf.get_width())//2, line_height))
                else:
                    raise ValueError("Invalid justify argument")

                line_height += Text.font_cache[size].size(line)[1]
        else:
            # no wrap
            surface = Text.font_cache[size].render(text, 1, colour)
        return surface

    def render(self, surface, game):
        surface.blit(self.surface, (self.x, self.y))

    @staticmethod
    def _word_wrap(text, width, font):
        words = text.split(' ')
        lines = []
        cur_line = [words.pop(0)]
        while words:
            if font.size(' '.join(cur_line))[0] > width:
                lines.append(' '.join(cur_line[:-1]))
                cur_line = [cur_line[-1]]
            cur_line.append(words.pop(0))
        lines.append(' '.join(cur_line))
        return lines
