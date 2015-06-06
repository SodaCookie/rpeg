from pygame.transform import scale
from pygame import Surface, SRCALPHA

from classes.rendering.render_group import RenderGroup
from classes.rendering.button import Button, ButtonInfo
from classes.rendering.image import Image
from classes.rendering.text import Text, TextInfo
from classes.image_cache import ImageCache
import classes.rendering.view as view

class LootMenu(RenderGroup):

    def __init__(self, party, gold, items):
        super().__init__("loot", (view.get_resolution()[0]//2,
            view.SCALE*10))

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

        self.button_title_style = TextInfo(fontcolor=(255,255,255),
                                   fontsize=30,
                                   alignment=-1,
                                   h_anchor=1,
                                   v_anchor=-1,
                                   wrap=True,
                                   width=149*view.SCALE)

        self.loot_style = TextInfo(fontcolor=(255,255,255),
                                   fontsize=30,
                                   alignment=0,
                                   h_anchor=0,
                                   v_anchor=-1,
                                   wrap=True,
                                   width=149*view.SCALE);

        self.large_button_style = ButtonInfo(
            text_color=(255, 255, 255),
            h_text_color=(255, 255, 0),
            p_text_color=(0, 128, 0),
            d_text_color=(0, 0, 0),
            h_anchor=0,
            v_anchor=0)

        self.party = party
        self.gold = gold
        self.items = items
        self.render()

    def render(self):
        # Create new back
        tmp_surface = Surface((77, 115), SRCALPHA)
        tmp_surface.fill((255,255,255,0))
        displacement = 0

        if self.gold:
            gold_back = ImageCache.add("images/ui/loot_gold.png", True)
            tmp_surface.blit(gold_back, (0, displacement))
            displacement += gold_back.get_height()

        if self.items:
            if self.gold:
                displacement -= 1
            loot_top = ImageCache.add("images/ui/loot_top.png", True)
            tmp_surface.blit(loot_top, (0, displacement))
            displacement += loot_top.get_height()
            loot_middle = ImageCache.add("images/ui/loot_middle.png")
            tmp_surface.blit(loot_middle, (0,displacement), (0, 0, loot_middle.get_width(),round(len(self.items)*loot_middle.get_height()/4)))
            displacement += round(len(self.items)*loot_middle.get_height()/4)
            loot_bottom = ImageCache.add("images/ui/loot_bottom.png", True)
            tmp_surface.blit(loot_bottom, (0, displacement))
            displacement += loot_top.get_height()

        chosen_back = tmp_surface
        back_position = (0, 10*view.SCALE)
        title_position = (0, 10*view.SCALE)
        button_position = (0, (displacement+13)*view.SCALE)

        self.add(Image(
            pos = back_position,
            surface = scale(chosen_back, tuple([z * view.SCALE for z in chosen_back.get_size()])),
            h_anchor = 0,
            v_anchor = 1,
            alpha = True))

        self.add(Text(
            title_position,
            t_info=self.loot_style,
            text="Treasure"))
        displacement = 20*view.SCALE
        if self.gold:
            title_position = (view.get_resolution()[0]/2,
                              displacement)
            self.add(Text(
                title_position,
                t_info=self.loot_style,
                text="Gold - %dg + (%dg)"%(self.party.gold-self.gold, self.gold)))

        self.add(Button(
                button_position,
                on_pressed=self.delete(),
                t_info=self.button_title_style,
                b_info=self.large_button_style,
                text="CLOSE"))