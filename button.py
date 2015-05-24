import pygame
from text import Text
from controller import MouseController

class ButtonInfo:
    def __init__(self,
                 width,
                 height=0,
                 text_color = None,
                 h_text_color = None,
                 p_text_color = None,
                 d_text_color = None,
                 img=None,
                 hovered_img=None,
                 pressed_img=None,
                 disabled_img=None,
                 stretch=True,
                 tile=False,
                 h_anchor=1,
                 v_anchor=1):
        self.width = width
        self.height = height
        self.text_color = text_color
        self.h_text_color = h_text_color
        self.p_text_color = p_text_color
        self.d_text_color = d_text_color
        self.img = img
        self.hovered_img = hovered_img
        self.pressed_img = pressed_img
        self.disabled_img = disabled_img
        self.stretch = stretch  # Not implemented
        self.tile = tile        # Not implemented
        self.h_anchor = h_anchor
        self.v_anchor = v_anchor



class Button(Text, MouseController):
    NEUTRAL=0
    HOVERED=1
    PRESSED=2
    DISABLED=3

    def __init__(self,
                 pos,
                 on_pressed,
                 on_released,
                 text_info,
                 button_info,
                 enabled,
                 default_text = ""):
        Text.__init__(self, pos, text_info, default_text)
        MouseController.__init__(self)
        self.on_pressed = on_pressed
        self.on_released = on_released
        self.button_info = button_info
        self.toggle(enabled)
        if self.button_info.height == 0:
            self.button_info.height = self.get_height()[1]

    def delete(self):
        Text.delete(self)
        MouseController.delete(self)

    def toggle(self, enabled):
        if enabled:
            self.state = Button.NEUTRAL
            if self.button_info.text_color != None:
                self.text_info.fontcolor = self.button_info.text_color
        else:
            self.state = Button.DISABLED
            if self.button_info.d_text_color != None:
                self.text_info.fontcolor = self.button_info.d_text_color

    def draw(self, surface):
        if self.button_info.h_anchor < 0:
            x_offset = -self.button_info.width
        elif self.button_info.h_anchor > 0:
            x_offset = 0
        else:
            x_offset = -self.button_info.width / 2

        if self.button_info.v_anchor < 0:
            y_offset = -self.button_info.height
        elif self.button_info.v_anchor > 0:
            y_offset = 0
        else:
            y_offset = -self.button_info.height / 2

        pos = (self.pos[0] + x_offset, self.pos[1] + y_offset)

        if self.state == Button.DISABLED and self.button_info.disabled_img != None:
            surface.blit(self.button_info.disabled_img, pos)
        elif self.state == Button.NEUTRAL and self.button_info.img != None:
            surface.blit(self.button_info.img, pos)
        elif self.state == Button.HOVERED and self.button_info.hovered_img != None:
            surface.blit(self.button_info.hovered_img, pos)
        elif self.state == Button.PRESSED and self.button_info.pressed_img != None:
            surface.blit(self.button_info.pressed_img, pos)

        Text.draw(self, surface)

    def mouse_motion(self, buttons, pos, rel):
        if self.state == Button.DISABLED:
            return
        
        if self.button_info.h_anchor < 0:
            x_offset = self.button_info.width / 2
        elif self.button_info.h_anchor > 0:
            x_offset = -self.button_info.width / 2
        else:
            x_offset = 0

        if self.button_info.v_anchor < 0:
            y_offset = self.button_info.height / 2
        elif self.button_info.v_anchor > 0:
            y_offset = -self.button_info.height / 2
        else:
            y_offset = 0

        if self.pos[0] - self.button_info.width / 2 <= pos[0] + x_offset <= self.pos[0] + self.button_info.width / 2 and\
           self.pos[1] - self.button_info.height / 2 <= pos[1] + y_offset <= self.pos[1] + self.button_info.height / 2:
            if self.state == Button.NEUTRAL:
                self.state = Button.HOVERED
                if self.button_info.h_text_color != None:
                    self.text_info.fontcolor = self.button_info.h_text_color

        else:
            if self.state == Button.HOVERED:
                self.state = Button.NEUTRAL
                if self.button_info.text_color != None:
                    self.text_info.fontcolor = self.button_info.text_color

            if self.state == Button.PRESSED:
                self.state = Button.NEUTRAL
                if self.button_info.text_color != None:
                    self.text_info.fontcolor = self.button_info.text_color

    def mouse_button_down(self, button, pos):
        if self.state == Button.DISABLED:
            return

        if self.state == Button.HOVERED:
            self.state = Button.PRESSED
            if self.button_info.p_text_color != None:
                self.text_info.fontcolor = self.button_info.p_text_color
            if self.on_pressed != None:
                self.on_pressed()

    def mouse_button_up(self, button, pos):
        if self.state == Button.DISABLED:
            return

        if self.state == Button.PRESSED:
            self.state = Button.HOVERED
            if self.button_info.h_text_color != None:
                self.text_info.fontcolor = self.button_info.h_text_color
            if self.on_released != None:
                self.on_released()



if __name__ == "__main__":
    pass
