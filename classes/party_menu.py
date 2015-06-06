import random
from functools import partial

from pygame.transform import scale

from classes.rendering.render_group import RenderGroup
from classes.rendering.button import Button, ButtonInfo
from classes.rendering.image import Image
from classes.rendering.text import Text, TextInfo
from classes.image_cache import ImageCache
import classes.rendering.view as view

class StatBars(RenderGroup):

    def __init__(self, party):
        super().__init__("bars", (0, 0))
        self.party = party
        self.render()

    def render(self):
        # hardcoded to save space (width*SCALE, height*SCALE)
        health = scale(ImageCache.add("images/ui/health.png"), (128, 8))
        speed = scale(ImageCache.add("images/ui/speed.png"), (128, 8))

        for i, member in enumerate(self.party.players):
            self.add(Image((i*78*view.SCALE+43*view.SCALE, -42*view.SCALE),
                surface = health,
                width = round(health.get_width()*
                    member.current_health/
                    member.health),
                h_anchor = 1,
                v_anchor = 1))

            self.add(Image((i*78*view.SCALE+43*view.SCALE, -37*view.SCALE),
                surface = speed,
                width = round(speed.get_width()*member.action/
                    member.action_max),
                h_anchor = 1,
                v_anchor = 1))


class PartyMenu(RenderGroup):

    def __init__(self, party, set_char):
        super().__init__("party", (0, view.get_resolution()[1]))
        self.party = party
        self.player_bg = [ImageCache.add("images/ui/player_back1.png", True)]
        self.current_character = None
        self.bars = StatBars(self.party)
        self.set_char = set_char

        self.text_style = TextInfo(fontcolor=(255,255,255),
                                   fontsize=16,
                                   alignment=-1,
                                   h_anchor=1,
                                   v_anchor=1,
                                   wrap=True,
                                   width=149*view.SCALE)
        self.render()

    def render(self):

        # Create new ui for the players
        for i, member in enumerate(self.party.players):
            portrait = ImageCache.add(member.portrait, True)
            chosen_back = random.choice(self.player_bg).copy()
            chosen_back.blit(portrait, (0, 0))
            hover_back = ImageCache.add("images/ui/hover_player_back1.png", True).copy()
            hover_back.blit(portrait, (0, 0))
            hover_back = scale(hover_back, tuple([z*view.SCALE for z in
                                hover_back.get_size()]))
            chosen_back = scale(chosen_back, tuple([z*view.SCALE for z in
                                chosen_back.get_size()]))
            button_func = partial(self.set_char, member)

            self.add(Button(
                pos = (6*view.SCALE+i*(chosen_back.get_width()+5*view.SCALE)+chosen_back.get_width()//2, -5*view.SCALE-chosen_back.get_height()//2),
                img = chosen_back,
                hovered_img = hover_back,
                pressed_img = hover_back,
                disabled_img = chosen_back,
                on_pressed = button_func,
                h_anchor = 0,
                v_anchor = 0,
                alpha = True))

            self.add(Text((
                6*view.SCALE+i*chosen_back.get_width()+i*5*view.SCALE, -chosen_back.get_height()-10*view.SCALE), self.text_style,
                text=member.name))

        self.add(self.bars)