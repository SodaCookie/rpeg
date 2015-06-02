from functools import partial
import random
import copy

from pygame.transform import scale
import pygame

import view
from image_cache import ImageCache
from dragable import Dragable
from image import Image
from text import Text, TextInfo
from button import Button, ButtonInfo
from controller import BattleController
import objects.dungeon as dungeon
import objects.party as party
import objects.player as player
import objects.monster as monster
import objects.shop as shop
import objects.battle as battle

BATTLESTART = pygame.USEREVENT
BATTLETICK = pygame.USEREVENT + 1
BATTLESTOP = pygame.USEREVENT + 2

class Group:

    groups = {}

    def __init__(self, name, pos, back=None):
        self.renderables = []
        self.back = back
        self.pos = pos
        setattr(Group, name, self)

    def add(self, renderable):
        if renderable not in self.renderables:
            pos = renderable.pos
            renderable.move((self.pos[0]+pos[0], self.pos[1]+pos[1]))
            self.renderables.append(renderable)

    def remove(self, renderable):
        if renderable in self.renderables:
            pos = renderable.pos
            renderable.move((self.pos[0]-pos[0], self.pos[1]-pos[1]))
            self.renderables.remove(renderable)

    def display(self):
        for r in self.renderables:
            r.display()

    def delete(self):
        for r in self.renderables:
            r.delete()
        if self.back:
            self.renderables = [self.back]
        else:
            self.renderables = []


class GameMenu(BattleController):

    SCALE = 4 # 1:4 scale
    POWER_PER_LEVEL = 100

    def __init__(self):
        super().__init__()
        self.text_bg = [ImageCache.add("images/ui/text_back1.png", True)]
        self.player_bg = [ImageCache.add("images/ui/player_back1.png", True)]

        option_button = ImageCache.add("images/ui/button_back.png", True)
        option_button = scale(option_button,
            [z*GameMenu.SCALE for z in option_button.get_size()])
        button = ImageCache.add("images/menu/button500x120.png")
        button_h = ImageCache.add("images/menu/button_h500x120.png")
        button_p = ImageCache.add("images/menu/button_p500x120.png")
        button_d = ImageCache.add("images/menu/button_d500x120.png")
        players = [player.Player("Player Tester") for i in range(4)]

        self.level = 1
        self.power = self.level*GameMenu.POWER_PER_LEVEL
        self.dungeon = dungeon.Dungeon(self.level)
        self.party = party.Party(players)
        self.resolution = view.get_resolution()
        self.current_location = self.dungeon.start
        self.current_location.generate()
        self.event = self.current_location.get_event()
        self.current_dialog = None
        self.current_battle = None
        self.current_target = None
        self.current_char = players[0]

        self.text_style = TextInfo(fontcolor=(255,255,255),
                                   fontsize=16,
                                   alignment=-1,
                                   h_anchor=1,
                                   v_anchor=1,
                                   wrap=True,
                                   width=149*GameMenu.SCALE)
        self.title_style = TextInfo(fontcolor=(255,255,255),
                                   fontsize=30,
                                   alignment=-1,
                                   h_anchor=1,
                                   v_anchor=-1,
                                   wrap=True,
                                   width=149*GameMenu.SCALE)
        self.button_title_style = TextInfo(fontcolor=(255,255,255),
                                   fontsize=30,
                                   alignment=-1,
                                   h_anchor=0,
                                   v_anchor=0)
        self.option_style = TextInfo(fontcolor=(255,255,255),
                                   fontsize=24,
                                   alignment=-1,
                                   h_anchor=-1,
                                   v_anchor=1)
        self.loot_style = TextInfo(fontcolor=(255,255,255),
                                   fontsize=30,
                                   alignment=0,
                                   h_anchor=0,
                                   v_anchor=-1,
                                   wrap=True,
                                   width=149*GameMenu.SCALE);

        self.button_style = ButtonInfo(
            text_color=(255, 255, 255),
            h_text_color=(255, 255, 0),
            p_text_color=(0, 128, 0),
            d_text_color=(0, 0, 0));
        self.large_button_style = ButtonInfo(self.button_style, h_anchor=0, v_anchor=0);
        self.option_button_style = ButtonInfo(self.button_style,
            img=option_button,
            hovered_img=option_button,
            pressed_img=option_button,
            disabled_img=option_button,
            h_anchor=-1,
            v_anchor=1);

        self.background = Image((0,0), filename="images/ui/background.png", h_anchor=1, v_anchor=1)
        self.background.display()
        self.single_renderables = {} # add to single_renderables to control
                                     # small elements on the screen
        self.create_group("event", (6*GameMenu.SCALE, 10*GameMenu.SCALE))
        self.create_group("option", (self.resolution[0]-7*GameMenu.SCALE,
                                     5*GameMenu.SCALE))
        self.create_group("party", (0, self.resolution[1]))
        self.create_group("loot", (self.resolution[0]//2, 0))
        self.create_group("travel", (6*GameMenu.SCALE, 10*GameMenu.SCALE))
        self.create_group("shop", (self.resolution[0]//2, 10*GameMenu.SCALE),
            ImageCache.add("images/ui/shop_back.png", True),
            h_anchor=0, v_anchor=1)
        self.create_group("monster", (6*GameMenu.SCALE, 10*GameMenu.SCALE))
        self.create_group("battle_info", (6*GameMenu.SCALE, 5*GameMenu.SCALE),
            ImageCache.add("images/ui/battle_info.png", True),
            h_anchor=1, v_anchor=1)
        self.render_event(self.event)
        self.render_option()
        self.render_party()

    def battle(self, delta):
        self.render_party()
        self.render_monster()
        self.render_battle_info()
        for monster in self.current_battle.monsters:
            if monster.ready:
                monster.cast("hello", self.current_battle)

    def create_group(self, name, pos, back=None, **kwarg):
        """Create and return a new display group, optional bg
        parameter is giving. keyword args are passed onto the
        backgroup image object. Alpha is guarenteed True.
        All groups can be accessed via the Group classmethod
        get_group. Will scale the given image to SCALE"""
        new_group = Group(name, pos)
        if back:
            back = scale(back, [GameMenu.SCALE*z for z in back.get_size()])
            bg = Image(pos,
                       surface=back,
                       alpha=True,
                       **kwarg)
            new_group.back = bg
        return new_group

    def render_battle_info(self):
        Group.battle_info.delete()

        if self.current_battle and self.current_char:
            abilities = ImageCache.add("images/ui/abilities.png", True)
            abilities = scale(abilities, (abilities.get_width()*GameMenu.SCALE,
                abilities.get_height()*GameMenu.SCALE))
            health = scale(ImageCache.add("images/ui/health.png"), (128, 8))
            speed = scale(ImageCache.add("images/ui/speed.png"), (128, 8))
            portrait = ImageCache.add(self.current_char.portrait, True)
            portrait = scale(portrait, (portrait.get_width()*GameMenu.SCALE,
                portrait.get_height()*GameMenu.SCALE))

            Group.battle_info.add(Image((37*GameMenu.SCALE, 0),
                surface = portrait,
                h_anchor = 1,
                v_anchor = 1))

            Group.battle_info.add(Image((0, 0),
                surface = abilities,
                alpha = True,
                h_anchor = 1,
                v_anchor = 1))

            Group.battle_info.add(Text((3*GameMenu.SCALE, GameMenu.SCALE),
                         t_info = self.title_style,
                         v_anchor = 1,
                         text = self.current_char.name))

            Group.battle_info.add(Image((4*GameMenu.SCALE, 11*GameMenu.SCALE),
                surface = health,
                width = round(health.get_width()*
                    self.current_char.current_health/
                    self.current_char.health),
                h_anchor = 1,
                v_anchor = 1))

            Group.battle_info.add(Text((4*GameMenu.SCALE, 13*GameMenu.SCALE+2),
                         t_info = self.text_style,
                         v_anchor = 1,
                         text = "Health: %d/%d" % (self.current_char.get_cur_health(), self.current_char.get_max_health())))

            Group.battle_info.add(Image((4*GameMenu.SCALE, 19*GameMenu.SCALE),
                surface = speed,
                width = round(speed.get_width()*self.current_char.action/
                    self.current_char.action_max),
                h_anchor = 1,
                v_anchor = 1))

            Group.battle_info.add(Text((4*GameMenu.SCALE, 21*GameMenu.SCALE+2),
                         t_info = self.text_style,
                         v_anchor = 1,
                         text = "Action: %d/%d" % (self.current_char.action, self.current_char.action_max)))

            Group.battle_info.add(Text((3*GameMenu.SCALE, 50*GameMenu.SCALE),
                         t_info = self.title_style,
                         v_anchor = 1,
                         text = "Skills"))

        Group.battle_info.display()

    def render_monster(self):
        Group.monster.delete()

        health = scale(ImageCache.add("images/ui/health.png"), (128, 8))
        speed = scale(ImageCache.add("images/ui/speed.png"), (128, 8))

        for i, monster in enumerate(self.current_battle.monsters):
            x = self.resolution[0]/4+(self.resolution[0]*3/4)/\
                len(self.current_battle.monsters)/2+\
                (self.resolution[0]*3/4)/len(self.current_battle.monsters)*i
            y = self.resolution[1]/3*2

            Group.monster.add(Image(
                (round(x), round(y)-GameMenu.SCALE),
                h_anchor = 0,
                v_anchor = -1,
                surface = monster.surface,
                alpha = True))

            Group.monster.add(Text(
                (round(x), round(y-monster.surface.get_height())-10*GameMenu.SCALE),
                t_info = self.text_style,
                fontsize = 18,
                h_anchor = 0,
                v_anchor = -1,
                text=monster.name))

            Group.monster.add(Image(
                (round(x-health.get_width()/2), round(y-monster.surface.get_height())-6*GameMenu.SCALE),
                width = round(health.get_width()*monster.current_health/
                    monster.health),
                h_anchor = 1,
                v_anchor = -1,
                surface = health,
                alpha = True))

            Group.monster.add(Image(
                (round(x-speed.get_width()/2), round(y-monster.surface.get_height())-2*GameMenu.SCALE),
                width = round(speed.get_width()*monster.action/
                    monster.action_max),
                h_anchor = 1,
                v_anchor = -1,
                surface = speed,
                alpha = True))

        Group.monster.display()

    def render_option(self):
        Group.option.delete()
        button_position = (0, 0)
        Group.option.add(Button(
            button_position,
            on_pressed = self.render_travel,
            t_info = self.option_style,
            b_info = self.option_button_style,
            text = "Travel"))
        Group.option.display()

    def render_party(self):
        # Clean up previous dialogs
        Group.party.delete()
        # hardcoded to save space (width*SCALE, height*SCALE)
        health = scale(ImageCache.add("images/ui/health.png"), (128, 8))
        speed = scale(ImageCache.add("images/ui/speed.png"), (128, 8))
        # Create new ui for the players
        for i, member in enumerate(self.party.players):
            chosen_back = random.choice(self.player_bg).copy()
            chosen_back.blit(ImageCache.add(member.portrait, True), (0, 0))
            hover_back = ImageCache.add("images/ui/hover_player_back1.png", True)
            hover_back = scale(hover_back, tuple([z*GameMenu.SCALE for z in
                                hover_back.get_size()]))
            chosen_back = scale(chosen_back, tuple([z*GameMenu.SCALE for z in
                                chosen_back.get_size()]))
            chosen_back.blit(health, (37*GameMenu.SCALE, 5*GameMenu.SCALE),
                (0, 0, round(health.get_width()*member.current_health/
                member.health), health.get_height()))
            chosen_back.blit(speed, (37*GameMenu.SCALE, 10*GameMenu.SCALE),
                (0, 0, round(speed.get_width()*member.action/member.action_max), speed.get_height()))
            hover_back.blit(chosen_back, (GameMenu.SCALE, GameMenu.SCALE))
            button_func = partial(self.set_current_character, member)

            Group.party.add(Button(
                pos = (6*GameMenu.SCALE+i*(chosen_back.get_width()+5*GameMenu.SCALE)+chosen_back.get_width()//2, -5*GameMenu.SCALE-chosen_back.get_height()//2),
                img = chosen_back,
                hovered_img = hover_back,
                pressed_img = chosen_back,
                disabled_img = chosen_back,
                on_pressed = button_func,
                h_anchor = 0,
                v_anchor = 0,
                alpha = True))

            Group.party.add(Text((
                6*GameMenu.SCALE+i*chosen_back.get_width()+i*5*GameMenu.SCALE, -chosen_back.get_height()-10*GameMenu.SCALE), self.text_style,
                text=member.name))

        Group.party.display()

    def set_current_character(self, character):
        self.current_char = character

    def render_travel(self):
        # Clean up previous dialog if any
        if self.current_dialog is not Group.travel and\
                self.current_dialog is not None:
            return
        elif self.current_dialog is Group.travel:
            self.close_travel()
            return

        # Create new back
        chosen_back = random.choice(self.text_bg)
        position = (0, 0)
        Group.travel.add(Image(
            position,
            surface = scale(chosen_back, tuple([z * GameMenu.SCALE for z in chosen_back.get_size()])),
            h_anchor = 1,
            v_anchor = 1,
            alpha = True))

        # Create new dialog
        Group.travel.add(Text((0, 0),
                               t_info=self.title_style,
                               text="Travel"))
        body = Text((5*GameMenu.SCALE, 5*GameMenu.SCALE),
                     t_info=self.text_style,
                     text="You are traveling...")
        Group.travel.add(body)
        displacement = body.get_size()[1]+9*GameMenu.SCALE
        choices = self.current_location.get_neighbours()
        for i, choice in enumerate(choices):
            button_func = partial(self.travel, choice)
            choice = Button(
                (5*GameMenu.SCALE, displacement),
                on_pressed=button_func,
                t_info=copy.copy(self.text_style),
                b_info=copy.copy(self.button_style),
                text="%d. %s"%(i+1, choice.loc_type))
            Group.travel.add(choice)
            displacement += choice.get_size()[1]+1*GameMenu.SCALE

        Group.travel.display()
        self.current_dialog = Group.travel

    def travel(self, location):
        if self.single_renderables.get("shop"):
            self.single_renderables["shop"].delete()
            self.single_renderables.pop("shop")
        self.current_location = location
        self.current_location.generate()
        Group.travel.delete()
        self.event = self.current_location.get_event()
        self.render_event(self.event)

    def render_event(self, dialog):
        # Clean up previous dialog if any
        if self.current_dialog is not Group.shop and\
                self.current_dialog is not None: # event is overriding
            self.current_dialog.delete()
        else:
            Group.event.delete()
        self.event = dialog

        #there is no more dialog
        if not dialog:
            return

        # Create new back
        chosen_back = random.choice(self.text_bg)
        Group.event.add(Image(
            pos = (0, 0),
            surface = scale(chosen_back, tuple([z * GameMenu.SCALE for z in chosen_back.get_size()])),
            h_anchor = 1,
            v_anchor = 1,
            alpha = True))

        # Create new dialog
        Group.event.add(Text((GameMenu.SCALE, 0),
                    self.title_style,
                    text=self.current_location.get_event_name().title()))
        body = Text((5*GameMenu.SCALE, 5*GameMenu.SCALE),
                     self.text_style,
                     text=self.event.body)

        Group.event.add(body)
        displacement = body.get_size()[1]+9*GameMenu.SCALE
        choices = self.event.get_choices(self.party)
        for i, choice in enumerate(choices):
            button_func = partial(self.render_event,
                                  self.event.make_choice(choice))
            choice = Button(
                (5*GameMenu.SCALE, displacement), True,
                copy.copy(self.text_style), copy.copy(self.button_style),
                on_pressed=button_func, text="%d. %s"%(i+1, choice))
            Group.event.add(choice)
            displacement += choice.get_size()[1]+1*GameMenu.SCALE
        if not choices:
            Group.event.add(Button(
                (5*GameMenu.SCALE, displacement), True,
                copy.copy(self.text_style), copy.copy(self.button_style),
                on_pressed=self.close_event,
                text="Next"))
        Group.event.display()
        self.current_dialog = Group.event

    def render_shop(self, shop):
        # Clean up previous dialog if any
        if self.current_dialog is not Group.shop and\
                self.current_dialog is not None:
            return
        elif self.current_dialog is Group.shop:
            self.close_shop()
            return

        Group.shop.delete()
        button_position = (self.resolution[0]-7*GameMenu.SCALE,
                           (15+5)*GameMenu.SCALE)
        button_func = partial(self.render_shop, shop)

        if not self.single_renderables.get("shop"):
            self.single_renderables["shop"] = Button(button_position,
                on_pressed = button_func, t_info = self.option_style,
                b_info = self.option_button_style, text = "Shop")
            self.single_renderables["shop"].display()

        Group.shop.add(Text((0, 0), t_info=self.title_style, text=shop.name,
                             h_anchor=0))
        Group.shop.add(Button((0, 0*GameMenu.SCALE+Group.shop.back.height),
                             on_pressed=self.close_shop,
                             b_info=self.large_button_style,
                             t_info=self.title_style,
                             text="CLOSE",
                             h_anchor=0,
                             v_anchor=1,
                             text_h_anchor=0,
                             text_v_anchor=1))

        for i, pair in enumerate(shop.items):
            item, value = pair
            Group.shop.add(Dragable(
                (-73*GameMenu.SCALE, 4*GameMenu.SCALE+i*20*GameMenu.SCALE),
                filename="images/item/test_icon.png",
                alpha=True,
                h_anchor=1,
                v_anchor=1,
                on_released=self.move_item))
            Group.shop.add(Text(
                (-55*GameMenu.SCALE, 4*GameMenu.SCALE+i*20*GameMenu.SCALE),
                t_info=self.text_style,
                text=item.name))
            Group.shop.add(Text(
                (-55*GameMenu.SCALE, 8*GameMenu.SCALE+i*20*GameMenu.SCALE),
                t_info=self.text_style,
                text="Price: %d"%value,
                fontsize=18,
                fontcolor=(255, 255, 51)))

        Group.shop.display()
        self.current_dialog = Group.shop

    def render_loot(self, items, gold):
        #Clean up
        if self.current_dialog is not Group.shop and\
                self.current_dialog is not None:
            return

        # Create new back
        tmp_surface = pygame.Surface((77, 115), SRCALPHA)
        tmp_surface.fill((255,255,255,0))
        displacement = 0

        if gold:
            gold_back = ImageCache.add("images/ui/loot_gold.png", True)
            tmp_surface.blit(gold_back, (0, displacement))
            displacement += gold_back.get_height()

        if items:
            if gold:
                displacement -= 1
            loot_top = ImageCache.add("images/ui/loot_top.png", True)
            tmp_surface.blit(loot_top, (0, displacement))
            displacement += loot_top.get_height()
            loot_middle = ImageCache.add("images/ui/loot_middle.png")
            tmp_surface.blit(loot_middle, (0,displacement), (0, 0, loot_middle.get_width(), round(len(items)*loot_middle.get_height()/4)))
            displacement += round(len(items)*loot_middle.get_height()/4)
            loot_bottom = ImageCache.add("images/ui/loot_bottom.png", True)
            tmp_surface.blit(loot_bottom, (0, displacement))
            displacement += loot_top.get_height()

        chosen_back = tmp_surface
        back_position = (0, 10*GameMenu.SCALE)
        title_position = (0, 10*GameMenu.SCALE)
        button_position = (0, (displacement+13)*GameMenu.SCALE)

        Group.loot.add(Image(
            pos = back_position,
            surface = scale(chosen_back, tuple([z * GameMenu.SCALE for z in chosen_back.get_size()])),
            h_anchor = 0,
            v_anchor = 1,
            alpha = True))

        Group.loot.add(Text(
            title_position,
            t_info=self.loot_style,
            text="Treasure"))
        displacement = 20*GameMenu.SCALE
        if gold:
            title_position = (self.resolution[0]/2,
                              displacement)
            Group.loot.add(Text(
                title_position,
                t_info=self.loot_style,
                text="Gold - %dg + (%dg)"%(self.party.gold-gold, gold)))

        Group.loot.add(Button(
                button_position,
                on_pressed=self.close_loot,
                t_info=copy.copy(self.button_title_style),
                b_info=copy.copy(self.large_button_style),
                text="CLOSE"))

        Group.loot.display()
        self.current_dialog = Group.loot

    def close_event(self):
        Group.event.delete()
        self.current_dialog = None
        if self.event.action:
            self.handle_action(self.event.action)

    def close_loot(self):
        Group.loot.delete()
        self.current_dialog = None

    def close_shop(self):
        Group.shop.delete()
        self.current_dialog = None

    def close_travel(self):
        Group.travel.delete()
        self.current_dialog = None

    def close_loot(self):
        Group.loot.delete()
        self.current_dialog = None

    def handle_action(self, action):
        key = action.split(" ")[0]
        args = []
        if len(action) > 1:
            args = action.split(" ")[1:]

        gold = 0
        items = []

        if key == "battle":
            if args:
                pass
            pygame.event.post(pygame.event.Event(BATTLESTART))
            pygame.time.set_timer(BATTLETICK, 30)
            monsters = [monster.Monster(100) for i in range(4)]
            Group.option.delete()
            self.current_battle = battle.Battle(self.party, monsters)
            self.busy = True
        elif key == "addgold":
            gold = int(args[0])
            self.party.add_gold(gold)
        elif key == "takegold":
            pass
        elif key == "item":
            pass
        elif key == "reward":
            pass
        elif key == "shop":
            s = shop.Shop(self.power, *args)
            self.render_shop(s)
        elif key == "alter":
            pass
        if gold > 0 or items:
            self.render_loot(items, gold)

    def move_item(self, item):
        pass