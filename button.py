import pygame
from text import Text
from controller import MouseController

class ButtonInfo:
    def __init__(self, 
                 width, 
                 height, 
                 img, 
                 hovered_img, 
                 pressed_img, 
                 disabled_img, 
                 stretch=True, 
                 tile=False):
        self.width = width
        self.height = height
        self.img = img
        self.hovered_img = hovered_img
        self.pressed_img = pressed_img
        self.disabled_img = disabled_img
        self.stretch = stretch
        self.tile = tile



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

    def delete(self):
        Text.delete(self)
        MouseController.delete(self)

    def toggle(self, enabled):
        if enabled:
            self.state = Button.NEUTRAL
        else:
            self.state = Button.DISABLED

    def draw(self, surface):
        pos = (self.pos[0] - self.button_info.width / 2, self.pos[1] - self.button_info.height / 2)
        if self.state == Button.DISABLED:
            surface.blit(self.button_info.disabled_img, pos)
        elif self.state == Button.NEUTRAL:
            surface.blit(self.button_info.img, pos)
        elif self.state == Button.HOVERED:
            surface.blit(self.button_info.hovered_img, pos)
        elif self.state == Button.PRESSED:
            surface.blit(self.button_info.pressed_img, pos)

        Text.draw(self, surface)
        
    def mouse_motion(self, buttons, pos, rel):
        if self.state == Button.DISABLED:
            return

        if self.pos[0] - self.button_info.width / 2 <= pos[0] <= self.pos[0] + self.button_info.width / 2 and\
           self.pos[1] - self.button_info.height / 2 <= pos[1] <= self.pos[1] + self.button_info.height / 2:
            if self.state == Button.NEUTRAL:
                self.state = Button.HOVERED

        else:
            if self.state == Button.HOVERED:
                self.state = Button.NEUTRAL

            if self.state == Button.PRESSED:
                self.state = Button.NEUTRAL
    
    def mouse_button_down(self, button, pos):
        if self.state == Button.DISABLED:
            return

        if self.state == Button.HOVERED:
            self.state = Button.PRESSED
            if self.on_pressed != None:
                self.on_pressed()

    def mouse_button_up(self, button, pos):
        if self.state == Button.DISABLED:
            return

        if self.state == Button.PRESSED:
            self.state = Button.HOVERED
            if self.on_released != None:
                self.on_released()



if __name__ == "__main__":
    pass
