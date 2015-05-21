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
    def __init__(self, 
                 pos, 
                 on_pressed, 
                 text_info, 
                 button_info, 
                 enabled, 
                 default_text = ""):
        Text.__init__(self, pos, text_info, default_text)
        MouseController.__init__(self)
        self.on_pressed = on_pressed
        self.button_info = button_info
        self.enabled = enabled

    def draw(self, surface):
        pass



if __name__ == "__main__":
    x = Button([4, 5])

    print(x.pos)
