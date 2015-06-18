import random
from functools import partial

from pygame.transform import scale

from classes import controller
from classes.rendering.menu import Menu
from classes.rendering.button import Button, ButtonInfo
from classes.rendering.image import Image
from classes.rendering.text import Text, TextInfo
from classes.image_cache import ImageCache
import classes.rendering.view as view


class PlayerMenu(Menu, controller.MouseController):
    """Is anchored in the bottom left corner"""

    NEUTRAL=0
    HOVERED=1
    PRESSED=2

    def __init__(self, pos, index, game, render_info):
        Menu.__init__(self, "player", pos, game, render_info)
        controller.MouseController.__init__(self)

        self.player_bg = ImageCache.add("images/ui/player_back1.png", True)
        self.player_hover_bg = ImageCache.add("images/ui/hover_player_back1.png", True)
        self.health_img = scale(ImageCache.add("images/ui/health.png"), (128, 8))
        self.speed_img = scale(ImageCache.add("images/ui/speed.png"), (128, 8))
        self.width, self.height = self.player_bg.get_size()
        self.width, self.height = self.width*view.SCALE, self.height*view.SCALE
        self.index = index
        self.state = PlayerMenu.NEUTRAL
        self.hover = False # used to artificially induce hovering

        self.text_style = TextInfo(fontcolor=(255,255,255),
                                   fontsize=16,
                                   alignment=-1,
                                   h_anchor=1,
                                   v_anchor=1,
                                   wrap=True,
                                   width=149*view.SCALE)

        self.name = self.add(Text((0, -47*view.SCALE), self.text_style))
        self.render_hover = False

        self.health = self.add(Image((37*view.SCALE, -37*view.SCALE),
            surface = self.health_img,
            h_anchor = 1,
            v_anchor = 1))

        self.speed = self.add(Image((37*view.SCALE, -32*view.SCALE),
            surface = self.speed_img,
            h_anchor = 1,
            v_anchor = 1))

    def delete(self):
        Menu.delete(self)
        controller.MouseController.delete(self)

    def get_player(self):
        return self.game.party.players[self.index]

    def draw_before(self, screen):
        posx, posy = view.get_abs_pos(self)
        player = self.get_player()

        if player == None:
            return Menu.BREAK

        portrait = ImageCache.add(player.portrait, True)
        if self.render_hover and \
                not self.render_info.display_event:
            back = self.player_hover_bg.copy()
        elif self.state == PlayerMenu.NEUTRAL:
            back = self.player_bg.copy()
        else:
            back = self.player_bg.copy()

        back.blit(portrait, (0, 0))
        back = scale(back, (self.width, self.height))
        screen.blit(back, (posx, posy-self.height))

        self.name.text = player.name
        self.health.width = round(self.health_img.get_width()*
                player.get_cur_health()/player.get_max_health())
        self.speed.width = round(self.speed_img.get_width()*player.action/
                player.action_max)

    def mouse_motion(self, buttons, pos, rel):
        pposx, pposy = view.get_abs_pos(self)
        mposx, mposy = pos
        if pposx <= mposx <= pposx+self.width and\
                pposy-self.height <= mposy <= pposy:
            self.game.hover_character = self.get_player()
            if self.state == PlayerMenu.NEUTRAL:
                self.state = PlayerMenu.HOVERED
        else:
            if self.state == PlayerMenu.HOVERED:
                self.state = PlayerMenu.NEUTRAL

            if self.state == PlayerMenu.PRESSED:
                self.state = PlayerMenu.NEUTRAL

    def mouse_button_down(self, button, pos):
        if not self.visible or self.get_player() == None:
            return

        if self.state == PlayerMenu.HOVERED:
            self.state = PlayerMenu.PRESSED
            if self.game.current_character == self.get_player():
                self.game.current_character = None
            else:
                self.game.current_character = self.get_player()
            self.display_info()

    def mouse_button_up(self, button, pos):
        if not self.visible or self.get_player() == None:
            return

        if self.state == PlayerMenu.PRESSED:
            self.state = PlayerMenu.HOVERED

    def display_info(self):
        if self.render_info.display_travel:
            self.render_info.display_travel = False
        if self.render_info.display_loot:
            self.render_info.display_loot = False
        if self.render_info.display_shop:
            self.render_info.display_shop = False
            return
        if self.render_info.display_alter:
            self.render_info.display_alter = False
        self.render_info.display_info = True


class PartyMenu(Menu, controller.MouseController):

    def __init__(self, game, render_info):
        Menu.__init__(self, "party", (0, view.get_resolution()[1]),
                                   game, render_info)
        self.players = []
        res = view.get_resolution()
        for i in range(len(game.party.players)):
            self.players.append(self.add(PlayerMenu((6*view.SCALE+i*78*view.SCALE, -5*view.SCALE),
                i, game, render_info)))
        controller.MouseController.__init__(self)

    def delete(self):
        Menu.delete(self)
        controller.MouseController.delete(self)

    def mouse_motion(self, buttons, pos, rel):
        self.dehighlight_all()
        if self.game.hover_character in [p.get_player() for p in self.players]:
            if self.game.current_move:
                if self.game.current_move.cast_type in ["single"]:
                    self.highlight_player(self.game.hover_character)
                elif self.game.current_move.cast_type in ["group"]:
                    self.highlight_all()
                else: # Defaults to one
                    self.highlight_player(self.game.hover_character)
            else:
                self.highlight_player(self.game.hover_character)

    def draw_before(self, screen):
        if not self.render_info.display_party:
            self.hide()
            return Menu.BREAK
        self.show()

    def dehighlight_all(self):
        for p in self.players:
            p.render_hover = False

    def highlight_player(self, player):
        for p in self.players:
            if p.get_player() == player:
                p.render_hover = True
                break

    def highlight_all(self):
        for p in self.players:
            p.render_hover = True