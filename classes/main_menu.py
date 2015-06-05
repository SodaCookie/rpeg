import copy

import classes.rendering.view as view
from classes.image_cache import ImageCache
from classes.rendering.text import Text, TextInfo
from classes.rendering.button import Button, ButtonInfo
from classes.rendering.render_group import RenderGroup

class MainMenu(RenderGroup):
    def __init__(self, singleplayer):
        super().__init__("main")
        self.singleplayer = singleplayer
        self.render()

    def render(self):
        button = ImageCache.add("images/menu/button500x120.png")
        button_h = ImageCache.add("images/menu/button_h500x120.png")
        button_p = ImageCache.add("images/menu/button_p500x120.png")
        button_d = ImageCache.add("images/menu/button_d500x120.png")

        text_style = TextInfo(fontcolor=(255, 255, 255),
                              fontsize=50,
                              h_anchor=0,
                              v_anchor=0,
                              alignment=0)
        button_style = ButtonInfo(width=500, height=120,
                                  text_color=(255, 255, 255),
                                  h_text_color=(255, 255, 0),
                                  p_text_color=(0, 128, 0),
                                  d_text_color=(0, 0, 0),
                                  img=button,
                                  hovered_img=button_h,
                                  pressed_img=button_p,
                                  disabled_img=button_d,
                                  h_anchor=0,
                                  v_anchor=0)
        resolution = view.get_resolution()

        self.add(Text(
            (resolution[0] / 2, resolution[1] / 4),
            t_info = text_style,
            text = "RNG Kitty Blaster"))

        self.add(Button(
            (resolution[0] / 2, resolution[1] / 2),
            enabled = True,
            t_info = text_style,
            b_info = button_style,
            on_pressed = self.singleplayer,
            text = "Single Player"))

        self.add(Button(
            (resolution[0] / 2, resolution[1] / 4 * 3),
            enabled = True,
            t_info = text_style,
            b_info = button_style,
            text = "Multi Player"))