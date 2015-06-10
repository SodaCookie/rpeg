from pygame.transform import scale
from pygame import Surface, SRCALPHA

from classes.rendering.render_group import RenderGroup
from classes.rendering.button import Button, ButtonInfo
from classes.rendering.image import Image
from classes.rendering.text import Text, TextInfo
from classes.image_cache import ImageCache
import classes.rendering.view as view

class StatBars(RenderGroup):

    def __init__(self, monsters):
        super().__init__("bars", (0, 0))
        self.monsters = monsters
        self.render()

    def render(self):
        # hardcoded to save space (width*SCALE, height*SCALE)
        health = scale(ImageCache.add("images/ui/health.png"), (128, 8))
        speed = scale(ImageCache.add("images/ui/speed.png"), (128, 8))

        for i, monster in enumerate(self.monsters):
            if monster.fallen:
                continue

            x = view.get_resolution()[0]/4+(view.get_resolution()[0]*3/4)/\
                len(self.monsters)/2+\
                (view.get_resolution()[0]*3/4)/len(self.monsters)*i
            y = view.get_resolution()[1]/3*2-view.SCALE*5

            self.add(Image(
                (round(x-health.get_width()/2), round(y-monster.surface.get_height()*view.SCALE)-6*view.SCALE),
                width = round(health.get_width()*monster.current_health/
                    monster.health),
                h_anchor = 1,
                v_anchor = -1,
                surface = health,
                alpha = True))

            self.add(Image(
                (round(x-speed.get_width()/2), round(y-monster.surface.get_height()*view.SCALE)-2*view.SCALE),
                width = round(speed.get_width()*monster.action/
                    monster.action_max),
                h_anchor = 1,
                v_anchor = -1,
                surface = speed,
                alpha = True))


class MonsterMenu(RenderGroup):

    def __init__(self, monsters):
        super().__init__("monster", (6*view.SCALE, 10*view.SCALE))
        self.text_style = TextInfo(fontcolor=(255,255,255),
                                   fontsize=16,
                                   alignment=-1,
                                   h_anchor=1,
                                   v_anchor=1,
                                   wrap=True,
                                   width=149*view.SCALE)

        self.monsters = monsters
        self.bars = StatBars(self.monsters)
        self.render()

    def render(self):
        for i, monster in enumerate(self.monsters):

            if monster.fallen:
                continue

            x = view.get_resolution()[0]/4+(view.get_resolution()[0]*3/4)/\
                len(self.monsters)/2+\
                (view.get_resolution()[0]*3/4)/\
                len(self.monsters)*i
            y = view.get_resolution()[1]/3*2-view.SCALE*5

            self.add(Text(
                (round(x), round(y-monster.surface.get_height()*view.SCALE)-10*view.SCALE),
                t_info = self.text_style,
                fontsize = 18,
                h_anchor = 0,
                v_anchor = -1,
                text=monster.name))

            self.add(Image(
                (round(x), round(y)-view.SCALE),
                h_anchor = 0,
                v_anchor = -1,
                surface = scale(monster.surface,
                    (monster.surface.get_width()*view.SCALE,
                     monster.surface.get_height()*view.SCALE)),
                alpha = True))
        self.add(self.bars)