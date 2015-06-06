from pygame.transform import scale

from classes.rendering.render_group import RenderGroup
from classes.rendering.text import TextInfo
from classes.rendering.button import Button, ButtonInfo
from classes.image_cache import ImageCache
import classes.rendering.view as view

class SideBar(RenderGroup):
    """Special group where only single renderables are rendered"""

    def __init__(self, display_travel, display_shop):
        super().__init__("sidebar", (0, 0))

        option_button = ImageCache.add("images/ui/button_back.png", True)
        option_button = scale(option_button,
            [z*view.SCALE for z in option_button.get_size()])

        self.option_style = TextInfo(fontcolor=(255,255,255),
                                   fontsize=24,
                                   alignment=-1,
                                   h_anchor=-1,
                                   v_anchor=1)

        self.option_button_style = ButtonInfo(
            text_color=(255, 255, 255),
            h_text_color=(255, 255, 0),
            p_text_color=(0, 128, 0),
            d_text_color=(0, 0, 0),
            img=option_button,
            hovered_img=option_button,
            pressed_img=option_button,
            disabled_img=option_button,
            h_anchor=-1,
            v_anchor=1)

        self.travel = Button(
            (view.get_resolution()[0]-7*view.SCALE, 5*view.SCALE),
            on_pressed = display_travel,
            t_info = self.option_style,
            b_info = self.option_button_style,
            text = "Travel")

        self.shop = Button(
            (view.get_resolution()[0]-7*view.SCALE, 15*view.SCALE),
            on_pressed = display_shop,
            t_info = self.option_style,
            b_info = self.option_button_style,
            text = "Shop")

    def render(self):
        self.add(self.travel)
        self.add(self.shop)

