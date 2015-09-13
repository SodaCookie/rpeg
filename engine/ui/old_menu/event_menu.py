import random
from functools import partial

from pygame.transform import scale
from pygame import USEREVENT
import pygame

from classes.game.monster import Monster
from classes.game.battle import Battle
from classes.rendering.menu import Menu
from classes.rendering.button import Button, ButtonInfo
from classes.rendering.image import Image
from classes.rendering.text import Text, TextInfo
from classes.image_cache import ImageCache
import classes.rendering.view as view
import classes.controller as controller

class EventMenu(Menu):

    def __init__(self, game, render_info):
        super().__init__("event", (6*view.SCALE, 10*view.SCALE), game, render_info)
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

    def draw_before(self, surface):
        if not self.render_info.display_event:
            self.hide()
            return Menu.BREAK
        self.show()

        if self.current != self.game.current_event:
            self.render()
            self.current = self.game.current_event

    def render(self):
        self.clear()

        if self.game.current_event == None:
            return

        if self.render_info.display_event == False:
            return

        # Create new back
        chosen_back = self.event_bg.copy()
        self.add(Image(
            pos = (0, 0),
            surface = scale(chosen_back, tuple([z * view.SCALE for z in chosen_back.get_size()])),
            h_anchor = 1,
            v_anchor = 1,
            alpha = True))

        # Create new dialog
        self.add(Text((view.SCALE, 0),
                    self.title_style,
                    text=self.game.current_location.get_event_name().title()))

        body = Text((5*view.SCALE, 5*view.SCALE),
                     self.text_style,
                     text=self.game.current_event.body)
        self.add(body)

        displacement = body.get_size()[1]+9*view.SCALE
        choices = self.game.current_event.get_choices(self.game.party)
        for i, choice in enumerate(choices):
            button_func = partial(self.update_current_event,
                                  self.game.current_event.make_choice(choice))
            choice = Button(
                (5*view.SCALE, displacement), True,
                self.text_style, self.button_style,
                on_pressed=button_func, text="%d. %s"%(i+1, choice))
            self.add(choice)
            displacement += choice.get_size()[1]+1*view.SCALE
        if not choices:
            self.add(Button(
                (5*view.SCALE, displacement), True,
                self.text_style, self.button_style,
                on_pressed=self.close_event,
                text="Next"))

    def update_current_event(self, event):
        self.game.current_event = event

    def close_event(self):
        if self.game.current_event.action:
            self.handle_action(self.game.current_event.action)
        self.game.current_event = None
        self.render_info.display_event = False
        self.game.current_character = None

    def handle_action(self, action):
        key = action.split(" ")[0]
        args = []
        if len(action) > 1:
            args = action.split(" ")[1:]

        if key == "battle":
            pygame.event.post(pygame.event.Event(controller.BATTLESTART))
            pygame.time.set_timer(controller.BATTLETICK, 30)
            self.game.monsters = self.create_monsters(*args)
            self.game.battle = Battle(self.game.party, self.game.monsters)
            self.display_monsters()
        elif key == "addgold":
            pass
        elif key == "takegold":
            pass
        elif key == "reward":
            gold = int(args[0])
            items = list(args[1])
        elif key == "shop":
            self.game_menu.create_shop()
            self.game_menu.display_shop()
        elif key == "alter":
            pass

    def display_monsters(self):
        self.render_info.display_monster = True
        self.render_info.display_party = True
        self.render_info.display_info = True

        self.render_info.display_travel = False
        self.render_info.display_shop = False
        self.render_info.display_loot = False
        self.render_info.display_event = False
        self.render_info.display_alter = False
        self.render_info.display_option = False

    def create_alter(self):
        pass

    def create_loot(self, gold, items):
        self.loot_menu = LootMenu(self.party, gold, items)
        self.sidebar.loot.display()

    def create_monsters(self, count=3, mtypes="", names="",
                        difficulties=Monster.COMMON, monsters=[]):
        if not monsters:
            for i in range(count):
                if mtypes and type(mtypes) == str:
                    mtype = mtypes
                elif mtypes and type(mtypes) == list:
                    mtype = mtypes[i]
                else:
                    mtype = ""

                if names and type(names) == str:
                    name = names
                elif names and type(names) == list:
                    name = names[i]
                else:
                    name = "Monster"

                if difficulties and type(difficulties) == int:
                    difficulty = difficulties
                elif difficulties and type(difficulties) == list:
                    difficulty = difficulties[i]
                else:
                    roll = random.random()
                    if roll > 0.9:
                        difficulty = Monster.BOSS
                    elif roll > 0.6:
                        difficulty = Monster.ELITE
                    else:
                        difficulty = Monster.COMMON

                monsters.append(Monster(self.game.power, difficulty, mtype, name))
        return monsters

    def create_battle(self):
        pass

    def create_shop(self):
        pass