from copy import copy

import pygame

import classes.rendering.view as view
from classes.rendering.text import Text
from classes.controller import MouseController

class ButtonInfo(dict):
    def __init__(self, b_info=None, **kwarg):
        # h_text_color = hover, p_text_color = press, d_text_color = disable
        super().__init__(self)
        self["width"] = None
        self["height"] = None
        self["text_color"] = None
        self["h_text_color"] = None
        self["p_text_color"] = None
        self["d_text_color"] = None
        self["img"] = None
        self["hovered_img"] = None
        self["pressed_img"] = None
        self["disabled_img"] = None
        self["stretch"] = True
        self["tile"] = False
        self["h_anchor"] = 1
        self["v_anchor"] = 1
        self["on_released"] = None
        self["on_hovered"] = None
        self["on_pressed"] = None
        if b_info: self.update(b_info)
        self.update(kwarg)

    def update(self, other):
        other = {key: other[key] for key in self.keys() if key in other}
        super().update(other)
        self.__dict__ = self


class Button(Text, MouseController):
    NEUTRAL=0
    HOVERED=1
    PRESSED=2
    DISABLED=3

    def __init__(self, pos, enabled=True, t_info=None, b_info=None, **kwarg):
        MouseController.__init__(self)
        # initiate text
        text_kwarg = {key.replace("text_", "", 1): kwarg[key]
            for key in kwarg.keys() if key.startswith("text_")} # get text keys
        if kwarg.get("text"): # special hook for simplicity
            text_kwarg["text"] = kwarg["text"]

        Text.__init__(self, pos, t_info, **text_kwarg)

        if b_info:
            self.button_info = copy(b_info)
        else:
            self.button_info = ButtonInfo(**kwarg)
        self.button_info.update(kwarg)

        self.toggle(enabled)
        if self.button_info.height == None:
            self.button_info.height = self.get_size()[1]
        if self.button_info.width == None:
            self.button_info.width = self.get_size()[0]

    @property
    def on_pressed(self):
        return self.button_info.on_pressed

    @property
    def on_released(self):
        return self.button_info.on_released

    def delete(self):
        Text.delete(self)
        MouseController.delete(self)

    def get_size(self):
        width = 0
        height = 0
        if self.button_info.img:
            width = self.button_info.img.get_width()
            height = self.button_info.img.get_height()
        width = max(super().get_size()[0], width)
        height = max(super().get_size()[1], height)
        return (width, height)

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
        if not self.visible:
            return

        abs_pos = view.get_abs_pos(self)
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

        pos = (abs_pos[0] + x_offset, abs_pos[1] + y_offset)

        if self.state == Button.DISABLED and self.button_info.disabled_img != None:
            surface.blit(self.button_info.disabled_img, pos)
        elif self.state == Button.NEUTRAL and self.button_info.img != None:
            surface.blit(self.button_info.img, pos)
        elif self.state == Button.HOVERED and self.button_info.hovered_img != None:
            surface.blit(self.button_info.hovered_img, pos)
        elif self.state == Button.PRESSED and self.button_info.pressed_img != None:
            surface.blit(self.button_info.pressed_img, pos)

        # HORRIBE CODE, MIGHT REWRITE AFTER SOME MORE THOUGHT
        # old_pos = abs_pos
        # if self.text_info.h_anchor == self.button_info.h_anchor:
        #     x_offset = abs_pos[0] # don't move anything we're good
        # else:
        #     if self.text_info.h_anchor < 0:
        #         x_offset = -self.height
        #     elif self.text_info.h_anchor > 0:
        #         x_offset = 0
        #     else:
        #         x_offset = -self.height / 2

        # if self.text_info.v_anchor < 0:
        #     y_offset = -self.height
        # elif self.text_info.v_anchor > 0:
        #     y_offset = 0
        # else:
        #     y_offset = -self.height / 2

        Text.draw(self, surface)

    def mouse_motion(self, buttons, pos, rel):
        if self.state == Button.DISABLED:
            return

        abs_pos = view.get_abs_pos(self)

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

        if abs_pos[0] - self.button_info.width / 2 <= pos[0] + x_offset <= abs_pos[0] + self.button_info.width / 2 and\
           abs_pos[1] - self.button_info.height / 2 <= pos[1] + y_offset <= abs_pos[1] + self.button_info.height / 2:
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
        if not self.visible:
            return

        if self.state == Button.DISABLED:
            return

        if self.state == Button.HOVERED:
            self.state = Button.PRESSED
            if self.button_info.p_text_color != None:
                self.text_info.fontcolor = self.button_info.p_text_color
            if self.on_pressed != None:
                self.on_pressed()

    def mouse_button_up(self, button, pos):
        if not self.visible:
            return

        if self.state == Button.DISABLED:
            return

        if self.state == Button.PRESSED:
            self.state = Button.HOVERED
            if self.button_info.h_text_color != None:
                self.text_info.fontcolor = self.button_info.h_text_color
            if self.on_released != None:
                self.on_released()



if __name__ == "__main__":
    pygame.font.init()
    b = Button((0, 0), text="hello world")
