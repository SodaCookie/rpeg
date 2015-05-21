from pygame import font
from view import Renderable


"""
Struct for condensing text parameters
"""
class TextInfo:
    """
    For anchors (and alignment) negative values represent left/bottom, 
    zero represents middle, and positive represents right/top.
    """
    def __init__(self, 
                 fontcolor=(0,0,0), 
                 fontname="fonts/VT323-Regular.ttf", 
                 fontsize=12, 
                 h_anchor=1, 
                 v_anchor=1, 
                 alignment=-1,
                 width=0, 
                 height=0,
                 wrap=False,
                 sensitive=False):
        self.fontcolor = fontcolor
        self.fontname = fontname
        self.fontsize = fontsize
        self.h_anchor = h_anchor
        self.v_anchor = v_anchor
        self.alignment = alignment
        self.width = width
        self.height = height
        self.wrap = wrap
        self.sensitive = sensitive


"""
The text class is a widget that gives you tools to render text
"""
class Text(Renderable):
    def __init__(self, 
                 pos, 
                 text_info, 
                 default_text=""):
        Renderable.__init__(self, pos)
        self.text_info = text_info
        self.text = default_text
        self.font = font.Font(text_info.fontname, text_info.fontsize)

    def draw(self, surface):
        f_surf = self.font.render(self.text, True, self.text_info.fontcolor)
        
        lines = self.text.split('\n')

        # Star out sensitive information
        if self.text_info.sensitive:
            for i in range(len(lines)):
              lines[i] = "".join("*" for j in range(len(lines[i])))

        # Wrap text if necessary
        if self.text_info.wrap:
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
                
        # Decide on where to put each line of text. Anchors define the
        # x_offset, y_offset variables and alignment decides the align
        # variable.
        max_width = 0
        for i in range(len(lines)):
            line_width = self.font.size(lines[i])[0]
            if line_width > max_width:
                max_width = line_width

        if self.text_info.wrap:
            if self.text_info.h_anchor < 0:
                x_offset = -self.text_info.width
            elif self.text_info.h_anchor > 0:
                x_offset = 0
            else:
                x_offset = -self.text_info.width / 2
        else:

            if self.text_info.h_anchor < 0:
                x_offset = -max_width
            elif self.text_info.h_anchor > 0:
                x_offset = 0
            else:
                x_offset = -max_width / 2.0

        if self.text_info.v_anchor < 0:
            y_offset = -self.text_info.fontsize * len(lines)
        elif self.text_info.v_anchor > 0:
            y_offset = 0
        else:
            y_offset = -self.text_info.fontsize * len(lines) / 2.0
            
        if self.text_info.alignment < 0:
            align = 0

        # Iterate over the lines of text to draw them.
        for i in range(len(lines)):
            if self.text_info.alignment > 0:
                align = max_width - self.font.size(lines[i])[0]
            elif self.text_info.alignment == 0:
                align = (max_width - self.font.size(lines[i])[0]) / 2.0

            surface.blit(self.font.render(lines[i], True, self.text_info.fontcolor), 
                            (x_offset + self.pos[0] + align, 
                             y_offset + self.pos[1] + self.text_info.fontsize * i))
        

if __name__ == "__main__":
    pass
