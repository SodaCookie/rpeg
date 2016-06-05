from functools import lru_cache

import pygame

LEFT = "left"
RIGHT = "right"
CENTER = "center"

@lru_cache()
def draw_image(filename):
    return pygame.image.load(filename).convert_alpha()

def draw_text(text, font, colour, width=None, textwrap=True, justify=LEFT):
    """Returns a drawn surface of a text given a font. """
    if width is not None and width > 0:
        # Text wrapping
        lines = []
        for paragraph in map(
                lambda line: _word_wrap(line, width, font),
                text.split('\n')):
            lines.extend(paragraph)
        height = sum(font.size(line)[1] for line in lines)
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        # drawing the line
        line_height = 0
        for line in lines:
            tmp_line_surf = font.render(line, 1, colour)
            if justify == LEFT:
                surface.blit(tmp_line_surf, (0, line_height))
            elif justify == RIGHT:
                surface.blit(tmp_line_surf,
                    (width - tmp_line_surf.get_width(), line_height))
            elif justify == CENTER:
                surface.blit(tmp_line_surf,
                    ((width - tmp_line_surf.get_width()) // 2, line_height))
            else:
                raise ValueError("Invalid justify argument")

            line_height += font.size(line)[1]
    else:
        surface = font.render(text, 1, colour)
    return surface

def draw_rect(width, height, colour):
    """Returns a coloured surface of size width and height."""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill(colour)
    return surface

def _word_wrap(text, width, font):
    """Helper function. Breaks string into a list of strings based on width
    specified"""
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
