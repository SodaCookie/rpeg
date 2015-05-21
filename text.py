from pygame import font
from view import Renderable


"""
Struct for condensing text parameters
"""
class TextInfo:
    """
    For anchors negative values represent left/bottom, 
    zero represents middle, and positive represents right/top.
    """
    def __init__(self, 
                 fontcolor=(0,0,0), 
                 fontname="ariel", 
                 fontsize=12, 
                 h_anchor=0, 
                 v_anchor=0, 
                 width=0, 
                 height=0,
                 wrap=False,
                 sensitive=False):
        self.fontcolor = fontcolor
        self.fontname = fontname
        self.fontsize = fontsize
        self.h_anchor = h_anchor
        self.v_anchor = v_anchor
        self.width = width
        self.height = height
        self.wrap = wrap
        self.sensitive = sensitive


"""
The text class is a widget that gives you tools to render text
"""
class Text(Renderable):
    def __init__(self, pos, text_info, default_text=""):
        Renderable.__init__(self, pos)
        self.text_info = text_info
        self.text = default_text
        self.font = font.Font(text_info.fontname, text_info.fontsize)

    def draw(self, surface):
        f_surf = self.font.render(self.text, True, self.text_info.fontcolor)

        if self.text_info.wrap:
            lines = text.split('\n')
            j = 0
            while j < len(lines):
                i = 0
                words = lines[j].split(' ')
                while i < len(words):
                    line_size = self.font.size(' '.join(words[:i+1]))[0]
                    if line_size > self.text_info.width:
                        lines = lines[:j]+[' '.join(words[:i-1])]+[' '.join(words[i-1:])]+lines[j+1:]
                        break
                    i += 1
                j += 1
                
            if text_info.h_anchor < 0:
                x_offset = -self.text_info.width
            elif text_info.h_anchor > 0:
                x_offset = 0
            else:
                x_offset = -self.text_info.width / 2

            if text_info.v_anchor < 0:
                y_offset = -self.text_info.fontsize * len(lines)
            elif text_info.v_anchor > 0:
                y_offset = 0
            else:
                y_offset = -self.text_info.fontsize * len(lines) / 2

            for i in range(len(lines)):
                surface.blit(self.font.render(lines[i], True, self.text_info.fontcolor), 
                             (x_offset + self.pos.x, 
                              y_offset + self.pos.y + self.text_info.fontsize * i))
        else:
            pass
        

if __name__ == "__main__":
    pass
