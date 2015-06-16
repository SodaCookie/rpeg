import random
from functools import partial

from pygame.transform import scale

from classes.rendering.menu import Menu
from classes.rendering.button import Button, ButtonInfo
from classes.rendering.image import Image
from classes.rendering.text import Text, TextInfo
from classes.image_cache import ImageCache
import classes.rendering.view as view

class TravelMenu(Menu):

    def __init__(self, game, render_info):
        super().__init__("travel", (6*view.SCALE, 10*view.SCALE), game, render_info)
        self.event_bg = ImageCache.add("images/ui/text_back1.png", True)
        self.current = None
        self.title_style = TextInfo(fontcolor=(255,255,255),
                                   fontsize=30,
                                   alignment=-1,
                                   h_anchor=1,
                                   v_anchor=-1,
                                   wrap=True,
                                   width=149*view.SCALE)

        self.text_style = TextInfo(fontcolor=(255,255,255),
                                   fontsize=16,
                                   alignment=-1,
                                   h_anchor=1,
                                   v_anchor=1,
                                   wrap=True,
                                   width=149*view.SCALE)

        self.button_style = ButtonInfo(
                                   text_color=(255, 255, 255),
                                   h_text_color=(255, 255, 0),
                                   p_text_color=(0, 128, 0),
                                   d_text_color=(0, 0, 0))

    def draw_before(self, screen):
        if not self.render_info.display_travel:
            self.hide()
            return Menu.BREAK
        self.show()

        if self.current != self.game.current_location:
            self.render()
            self.current = self.game.current_location

    def travel(self, location):
        """Returns given location"""
        self.game.current_location = location
        self.game.current_location.generate()
        self.game.current_event = self.game.current_location.get_event()
        self.render_info.display_event = True
        self.render_info.display_travel = False

    def render(self):
        self.clear()
        # Create new back
        chosen_back = self.event_bg
        self.add(Image(
            (0, 0),
            surface = scale(chosen_back, tuple([z * view.SCALE for z in chosen_back.get_size()])),
            h_anchor = 1,
            v_anchor = 1,
            alpha = True))

        # Create new dialog
        self.add(Text((0, 0),
                 t_info=self.title_style,
                 text="Travel"))
        body = Text((5*view.SCALE, 5*view.SCALE),
                     t_info=self.text_style,
                     text="You are traveling...")
        self.add(body)
        displacement = body.get_size()[1]+9*view.SCALE
        choices = self.game.current_location.get_neighbours()

        for i, choice in enumerate(choices):
            button_func = partial(self.travel, choice)
            choice = Button(
                (5*view.SCALE, displacement),
                on_pressed=button_func,
                t_info=self.text_style,
                b_info=self.button_style,
                text="%d. %s"%(i+1, choice.loc_type))
            self.add(choice)
            displacement += choice.get_size()[1]+1*view.SCALE