from pygame.transform import scale
from pygame import Surface, SRCALPHA
import pygame

import classes.game.player as player
from classes.rendering.render_group import RenderGroup
from classes.rendering.button import Button, ButtonInfo
from classes.rendering.image import Image
from classes.rendering.text import Text, TextInfo
from classes.image_cache import ImageCache
import classes.rendering.view as view

class StatBars(RenderGroup):

    def __init__(self, character):
        super().__init__("bars", (0, 0))

        self.text_style = TextInfo(fontcolor=(255,255,255),
                                   fontsize=16,
                                   alignment=-1,
                                   h_anchor=1,
                                   v_anchor=1,
                                   wrap=True,
                                   width=149*view.SCALE)

        self.character = character
        self.render()

    def render(self):
        # hardcoded to save space (width*SCALE, height*SCALE)
        health = scale(ImageCache.add("images/ui/health.png"), (128, 8))
        speed = scale(ImageCache.add("images/ui/speed.png"), (128, 8))

        if self.character:
            self.add(Image((4*view.SCALE, 11*view.SCALE),
                surface = health,
                width = round(health.get_width()*
                    self.character.current_health/
                    self.character.health),
                h_anchor = 1,
                v_anchor = 1))

            self.add(Text((4*view.SCALE, 13*view.SCALE+2),
                         t_info = self.text_style,
                         v_anchor = 1,
                         text = "Health: %d/%d" % (self.character.get_cur_health(), self.character.get_max_health())))

            self.add(Image((4*view.SCALE, 19*view.SCALE),
                surface = speed,
                width = round(speed.get_width()*self.character.action/
                    self.character.action_max),
                h_anchor = 1,
                v_anchor = 1))

            self.add(Text((4*view.SCALE, 21*view.SCALE+2),
                         t_info = self.text_style,
                         v_anchor = 1,
                         text = "Action: %d/%d" % (self.character.action, self.character.action_max)))


class Icons(RenderGroup):

    def __init__(self, character):
        super().__init__("icons", (0, 0))
        self.character = character
        self.render()

    def update(self, enable):
        for r in self.rendering:
            r.toggle(enable)

    def render(self):
        for i, move in enumerate(self.character.moves):
            if isinstance(self.character, player.Player):
                img = ImageCache.add(move.surface)
                h_img = img.copy()
                pygame.draw.rect(h_img, ((255, 255, 0)), h_img.get_rect(), 1)
                p_img = img.copy()
                pygame.draw.rect(p_img, (0, 128, 0), h_img.get_rect(), 1)
                d_img = img.copy()
                d_img.set_alpha(100)
                enable = True if self.character.ready else False

                self.add(Button(
                    (10*view.SCALE+i%3*20*view.SCALE,
                        65*view.SCALE+i//3*20*view.SCALE),
                    enabled = enable,
                    h_anchor = 1,
                    v_anchor = 1,
                    img = scale(img, (64, 64)),
                    hovered_img = scale(h_img, (64, 64)),
                    pressed_img = scale(p_img, (64, 64)),
                    disabled_img = scale(d_img, (64, 64)),
                    hover_img = scale(ImageCache.add(move.surface), (64, 64))))


class BattleInfoMenu(RenderGroup):

    def __init__(self, character, battle=False, limited=False):
        super().__init__("battle_info", (6*view.SCALE, 5*view.SCALE))

        self.title_style = TextInfo(fontcolor=(255,255,255),
                                   fontsize=30,
                                   alignment=-1,
                                   h_anchor=1,
                                   v_anchor=-1,
                                   wrap=True,
                                   width=149*view.SCALE)

        self.character = character
        self.battle = battle
        self.limited = limited
        self.bars = StatBars(character)
        self.icons = Icons(character)
        self.render()

    def render(self):

        if self.battle:
            # display smaller verison
            bg = ImageCache.add("images/ui/battle_info.png", True)
            bg = scale(bg, tuple((view.SCALE*z for z in bg.get_size())))
        else:
            # display larger version
            bg = ImageCache.add("images/ui/battle_info.png", True)
            bg = scale(bg, tuple((view.SCALE*z for z in bg.get_size())))

        self.add(Image(
            (0, 0),
            surface=bg,
            h_anchor=1,
            v_anchor=1,
            alpha=True))

        if self.character:
            abilities = ImageCache.add("images/ui/abilities.png", True)
            abilities = scale(abilities, (abilities.get_width()*view.SCALE,
                abilities.get_height()*view.SCALE))
            portrait = ImageCache.add(self.character.portrait, True)
            portrait = scale(portrait, (portrait.get_width()*view.SCALE,
                portrait.get_height()*view.SCALE))

            self.add(Image((37*view.SCALE, 0),
                surface = portrait,
                h_anchor = 1,
                v_anchor = 1))

            self.add(Image((0, 0),
                surface = abilities,
                alpha = True,
                h_anchor = 1,
                v_anchor = 1))

            self.add(Text((3*view.SCALE, view.SCALE),
                         t_info = self.title_style,
                         v_anchor = 1,
                         text = self.character.name))

            self.add(Text((3*view.SCALE, 50*view.SCALE),
                         t_info = self.title_style,
                         v_anchor = 1,
                         text = "Skills"))

            self.add(self.bars)
            self.add(self.icons)