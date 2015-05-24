import view
from image_cache import ImageCache
from text import Text, TextInfo
from button import Button, ButtonInfo
import copy

class MainMenu(object):
    def __init__(self, singleplayer):
        button = ImageCache.add("images/menu/button500x120.png")
        button_h = ImageCache.add("images/menu/button_h500x120.png")
        button_p = ImageCache.add("images/menu/button_p500x120.png")
        button_d = ImageCache.add("images/menu/button_d500x120.png")

        text_style = TextInfo(fontcolor=(255, 255, 255),
                              fontsize=50,
                              h_anchor=0,
                              v_anchor=0,
                              alignment=0);
        button_style = ButtonInfo(500, 120,
                                  (255, 255, 255),
                                  (255, 255, 0),
                                  (0, 128, 0),
                                  (0, 0, 0),
                                  button,
                                  button_h,
                                  button_p,
                                  button_d,
                                  h_anchor=0,
                                  v_anchor=0);

        resolution = view.get_resolution()

        self.title = Text((resolution[0] / 2, resolution[1] / 4), copy.copy(text_style), "RNG Kitty Blaster")
        self.single_player = Button((resolution[0] / 2, resolution[1] / 2), singleplayer, None, copy.copy(text_style), copy.copy(button_style), True, "Single Player")
        self.multi_player = Button((resolution[0] / 2, resolution[1] / 4 * 3), None, None, copy.copy(text_style), copy.copy(button_style), True, "Multi Player")

    def close(self):
        self.title.delete()
        self.single_player.delete()
        self.multi_player.delete()
