from functools import partial

from pygame.transform import scale
from pygame import Surface, SRCALPHA
import pygame

import classes.game.player as player
from classes.controller import MouseController
from classes.rendering.menu import Menu
from classes.rendering.button import Button, ButtonInfo
from classes.rendering.image import Image
from classes.rendering.text import Text, TextInfo
from classes.image_cache import ImageCache
import classes.rendering.view as view

class Icon(view.Renderable, MouseController):

    NEUTRAL = 0
    HOVERED = 1
    PRESSED = 2
    DISABLED = 3

    def __init__(self, pos, move, game, render_info):
        view.Renderable.__init__(self, pos)
        MouseController.__init__(self)
        self.state = Icon.NEUTRAL
        self.move = move
        self.game = game
        self.player_move = move
        self.width = ImageCache.add(move.surface).get_width() * view.SCALE
        self.height = ImageCache.add(move.surface).get_height() * view.SCALE
        self.render_info = render_info

    def delete(self):
        view.Renderable.delete(self)
        MouseController.delete(self)

    def mouse_motion(self, buttons, pos, rel):
        if not self.game.current_character.ready:
            return

        pposx, pposy = view.get_abs_pos(self)
        mposx, mposy = pos

        if pposx <= mposx <= pposx+self.width and\
                pposy <= mposy <= pposy+self.height:
            if self.state == Icon.NEUTRAL:
                self.state = Icon.HOVERED
        else:
            if self.state == Icon.HOVERED:
                self.state = Icon.NEUTRAL

            if self.state == Icon.PRESSED:
                self.state = Icon.NEUTRAL

    def mouse_button_down(self, button, pos):
        if not self.visible and not self.game.current_character.ready:
            return

        if self.state == Icon.HOVERED:
            self.state = Icon.PRESSED
            self.cast()

    def mouse_button_up(self, button, pos):
        if not self.visible and not self.game.current_character.ready:
            return

        if self.state == Icon.PRESSED:
            self.state = Icon.HOVERED

    def draw(self, screen):
        pos = view.get_abs_pos(self)
        img = ImageCache.add(self.player_move.surface).copy()

        if not self.game.current_character.ready:
            img.set_alpha(100)
        elif self.state == Icon.HOVERED:
            pygame.draw.rect(img, ((255, 255, 0)), img.get_rect(), 1)
        elif self.state == Icon.PRESSED:
            pygame.draw.rect(img, (0, 128, 0), img.get_rect(), 1)

        img = scale(img, (img.get_width()*view.SCALE,
            img.get_height()*view.SCALE))

        screen.blit(img, pos)

    def cast(self):
        self.game.current_move = self.move


class BattleInfoMenu(Menu):

    def __init__(self, game, render_info):
        Menu.__init__(self, "battle_info", (6*view.SCALE, 5*view.SCALE), game, render_info)

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

        self.health_img = scale(ImageCache.add("images/ui/health.png"), (128, 8))
        self.speed_img = scale(ImageCache.add("images/ui/speed.png"), (128, 8))
        self.current = None
        self.health = None
        self.health_text = None
        self.speed = None
        self.speed_text = None

    def render(self):
        self.clear()

        if self.game.current_character:
            abilities = ImageCache.add("images/ui/abilities.png", True)
            abilities = scale(abilities, (abilities.get_width()*view.SCALE,
                abilities.get_height()*view.SCALE))
            portrait = ImageCache.add(self.game.current_character.portrait, True)
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
                         text = self.game.current_character.name))

            self.add(Text((3*view.SCALE, 50*view.SCALE),
                         t_info = self.title_style,
                         v_anchor = 1,
                         text = "Skills"))

            self.health = self.add(Image((4*view.SCALE, 11*view.SCALE),
                surface = self.health_img,
                width = round(self.health_img.get_width()*
                    self.game.current_character.current_health/
                    self.game.current_character.health),
                h_anchor = 1,
                v_anchor = 1))

            self.health_text = self.add(Text((4*view.SCALE, 13*view.SCALE+2),
                         t_info = self.text_style,
                         v_anchor = 1,
                         text = "Health: %d/%d" % (self.game.current_character.get_cur_health(), self.game.current_character.get_max_health())))

            self.speed = self.add(Image((4*view.SCALE, 19*view.SCALE),
                surface = self.speed_img,
                width = round(self.speed_img.get_width()*self.game.current_character.action/
                    self.game.current_character.action_max),
                h_anchor = 1,
                v_anchor = 1))

            self.speed_text = self.add(Text((4*view.SCALE, 21*view.SCALE+2),
                         t_info = self.text_style,
                         v_anchor = 1,
                         text = "Action: %d/%d" % (self.game.current_character.action, self.game.current_character.action_max)))
            for i, move in enumerate(self.game.current_character.moves):
                x, y = i%3, i//3
                self.add(Icon((4*view.SCALE+view.SCALE*20*x, 60*view.SCALE+view.SCALE*20*y),
                    move, self.game, self.render_info))

    def draw_before(self, screen):
        if self.render_info.display_event or \
                not self.render_info.display_info or \
                not self.game.battle and not self.game.current_character:
            self.hide()
            return Menu.BREAK
        self.show()

        pos = view.get_abs_pos(self)

        if self.game.battle:
            # display smaller verison
            bg = ImageCache.add("images/ui/battle_info.png", True)
            bg = scale(bg, tuple((view.SCALE*z for z in bg.get_size())))
        else:
            # display larger version
            bg = ImageCache.add("images/ui/battle_info.png", True)
            bg = scale(bg, tuple((view.SCALE*z for z in bg.get_size())))
        screen.blit(bg, pos)

        if self.current != self.game.current_character:
            self.render()
            self.current = self.game.current_character

        if self.game.current_character:
            self.health.width = round(self.health_img.get_width()*
                        self.game.current_character.current_health/
                        self.game.current_character.health)
            self.speed.width = round(self.speed_img.get_width()*
                        self.game.current_character.action/
                        self.game.current_character.action_max)
            self.health_text.text = "Health: %d/%d" % (self.game.current_character.get_cur_health(), self.game.current_character.get_max_health())
            self.speed_text.text = "Action: %d/%d" % (self.game.current_character.action, self.game.current_character.action_max)