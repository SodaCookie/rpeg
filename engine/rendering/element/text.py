from copy import copy

from pygame import font

import classes.rendering.view as view
from classes.rendering.view import Renderable

"""
Struct for condensing text parameters
"""

class TextInfo(dict):
    def __init__(self, t_info=None, **kwarg):
        # h_text_color = hover, p_text_color = press, d_text_color = disable
        super().__init__(self)
        self["fontcolor"] = (0,0,0)
        self["fontname"] = "fonts/VT323-Regular.ttf"
        self["fontsize"] = 12
        self["h_anchor"] = 1
        self["v_anchor"] = 1
        self["alignment"] = 1
        self["width"] = None
        self["height"] = None
        self["wrap"] = False
        self["sensitive"] = False
        self["text"] = ""
        if t_info: self.update(t_info)
        self.update(kwarg)

    def update(self, other):
        other = {key: other[key] for key in self.keys() if key in other}
        super().update(other)
        self.__dict__ = self # magic line, beware of references ERIC


"""
The text class is a widget that gives you tools to render text
"""
class Text(Renderable):
    def __init__(self, pos, t_info=None, **kwarg):
        super().__init__(pos)
        if t_info:
            self.text_info = copy(t_info)
        else:
            self.text_info = TextInfo()
        self.text_info.update(kwarg)
        self.font = font.Font(self.text_info.fontname, self.text_info.fontsize)
        self.lines = self.text.split('\n')
        if self.text_info.wrap:
            self._wrap_text()

    @property
    def text(self):
        return self.text_info.text

    @text.setter
    def text(self, text):
        self.text_info.text = text
        self.lines = self.text.split('\n')
        if self.text_info.wrap:
            self._wrap_text()

    def delete(self):
        super().delete()

    def draw(self, surface):
        pos = view.get_abs_pos(self)
        # Star out sensitive information
        # (this is currently broken when used with text wrapping)
        if self.text_info.sensitive:
            for i in range(len(lines)):
              self.lines[i] = "".join("*" for j in range(len(self.lines[i])))

        # Decide on where to put each line of text. Anchors define the
        # x_offset, y_offset variables and alignment decides the align
        # variable.
        max_width = 0
        for i in range(len(self.lines)):
            line_width = self.font.size(self.lines[i])[0]
            if line_width > max_width:
                max_width = line_width

        if self.text_info.h_anchor < 0:
            x_offset = -max_width
        elif self.text_info.h_anchor > 0:
            x_offset = 0
        else:
            x_offset = -max_width / 2

        if self.text_info.v_anchor < 0:
            y_offset = -self.text_info.fontsize * len(self.lines)
        elif self.text_info.v_anchor > 0:
            y_offset = 0
        else:
            y_offset = -self.text_info.fontsize * len(self.lines) / 2

        if self.text_info.alignment < 0:
            align = 0

        # Iterate over the lines of text to draw them.
        for i in range(len(self.lines)):
            if self.text_info.alignment > 0:
                align = max_width - self.font.size(self.lines[i])[0]
            elif self.text_info.alignment == 0:
                align = (max_width - self.font.size(self.lines[i])[0]) / 2
            surface.blit(self.font.render(self.lines[i], True, self.text_info.fontcolor),
                            (x_offset + pos[0] + align,
                             y_offset + pos[1] + self.text_info.fontsize * i))

    def get_size(self):
        max_width = 0
        for i in range(len(self.lines)):
            line_width = self.font.size(self.lines[i])[0]
            if line_width > max_width:
                max_width = line_width

        return (max_width, len(self.lines) * self.text_info.fontsize);

    def _wrap_text(self):
        if self.text_info.wrap:
            j = 0
            while j < len(self.lines):
                i = 0
                words = self.lines[j].split(' ')
                while i < len(words):
                    line_size = self.font.size(' '.join(words[:i + 1]))[0]
                    if line_size > self.text_info.width:
                        self.lines = self.lines[:j] + [' '.join(words[:i - 1])] + [' '.join(words[i - 1:])] + self.lines[j + 1:]
                        break
                    i += 1
                j += 1



if __name__ == "__main__":
    font.init()
    text = Text((0, 0), text="hello world")
