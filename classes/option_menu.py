from pygame.transform import scale

from classes.rendering.menu import Menu
from classes.rendering.text import TextInfo
from classes.rendering.button import Button, ButtonInfo
from classes.image_cache import ImageCache
import classes.rendering.view as view

class OptionMenu(Menu):
    """Special group where only single renderables are rendered"""

    def __init__(self, game, render_info):
        super().__init__("option", (0, 0), game, render_info)

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

        self.travel = self.add(Button(
            (view.get_resolution()[0]-7*view.SCALE, 5*view.SCALE),
            on_pressed = self.display_travel,
            t_info = self.option_style,
            b_info = self.option_button_style,
            text = "Travel"))

        self.shop = self.add(Button(
            (view.get_resolution()[0]-7*view.SCALE, 20*view.SCALE),
            on_pressed = self.display_shop,
            t_info = self.option_style,
            b_info = self.option_button_style,
            text = "Shop"))

        self.loot = self.add(Button(
            (view.get_resolution()[0]-7*view.SCALE, 35*view.SCALE),
            on_pressed = self.display_loot,
            t_info = self.option_style,
            b_info = self.option_button_style,
            text = "Loot"))

    def hide_all(self):
        self.travel.hide()
        self.shop.hide()
        self.loot.hide()

    def draw_before(self, screen):
        self.hide_all()
        if self.render_info.display_event or self.render_info.display_monster:
            return Menu.BREAK

        if not self.render_info.display_option:
            return Menu.BREAK

        self.travel.show()

        if self.game.shop:
            self.shop.show()

        if self.game.loot:
            self.loot.show()

    def display_travel(self):
        if self.render_info.display_travel:
            self.render_info.display_travel = False
            return
        if self.render_info.display_loot:
            self.render_info.display_loot = False
        if self.render_info.display_shop:
            self.render_info.display_shop = False
        if self.render_info.display_alter:
            self.render_info.display_alter = False
        self.render_info.display_travel = True

    def display_loot(self):
        if self.render_info.display_travel:
            self.render_info.display_travel = False
        if self.render_info.display_loot:
            self.render_info.display_loot = False
            return
        if self.render_info.display_shop:
            self.render_info.display_shop = False
        if self.render_info.display_alter:
            self.render_info.display_alter = False
        self.render_info.display_travel = True

    def display_shop(self):
        if self.render_info.display_travel:
            self.render_info.display_travel = False
            return
        if self.render_info.display_loot:
            self.render_info.display_loot = False
        if self.render_info.display_shop:
            self.render_info.display_shop = False
            return
        if self.render_info.display_alter:
            self.render_info.display_alter = False
        self.render_info.display_travel = True

    def display_alter(self):
        if self.render_info.display_travel:
            self.render_info.display_travel = False
            return
        if self.render_info.display_loot:
            self.render_info.display_loot = False
        if self.render_info.display_shop:
            self.render_info.display_shop = False
        if self.render_info.display_alter:
            self.render_info.display_alter = False
            return
        self.render_info.display_travel = True
