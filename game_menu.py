from functools import partial
import random
import copy

from pygame.transform import scale
from pygame import Surface, SRCALPHA

import view
from image_cache import ImageCache
from dragable import Dragable
from image import Image
from text import Text, TextInfo
from button import Button, ButtonInfo
import objects.dungeon as dungeon
import objects.party as party
import objects.player as player
import objects.monster as monster

class LootDisplayData(dict):
    back = None
    gold = None
    title = None
    close = None

    @classmethod
    def delete(cls):
        if not cls.back:
            return
        if cls.back: cls.back.delete()
        if cls.gold: cls.gold.delete()
        if cls.title: cls.title.delete()
        if cls.close: cls.close.delete()
        cls.back = None
        cls.gold = None
        cls.title = None
        cls.close = None

class PlayerDisplayData(object):
    back = []
    portrait = []
    name = []
    health = []
    speed = []

    @classmethod
    def delete(cls):
        if not PlayerDisplayData.back:
            return
        for i in cls.back: i.delete()
        for i in cls.name: i.delete()
        for i in cls.portrait: i.delete()
        for i in cls.speed: i.delete()
        for i in cls.health: i.delete()
        cls.back = []
        cls.name = []
        cls.portrait = []
        cls.speed = []
        cls.health = []

class DialogDisplayData(object):
    back = None
    choices = []
    body = None
    title = None

    @classmethod
    def delete(cls):
        """Closes dialog and will activate any action pushed from event"""
        if cls.body:
            cls.back.delete()
            cls.body.delete()
            cls.title.delete()
            for choice in cls.choices:
                choice.delete()
        cls.back = None
        cls.choices = []
        cls.body = None
        cls.title = None

class TravelDisplayData(object):
    back = None
    body = None
    choices = []
    title = None
    #close = None

    @classmethod
    def delete(cls):
        if cls.body:
            cls.body.delete()
            cls.back.delete()
            for c in cls.choices: c.delete()
            #cls.close.delete()
            cls.title.delete()
        cls.body = None
        cls.back = None
        cls.choices = []
        cls.close = None
        cls.title = None

class OptionsDisplayData(object):
    travel = None

    @classmethod
    def delete(cls):
        if travel:
            cls.travel.delete()
        cls.travel = None

class BattleDisplayData(object):
    pass

class ShopDisplayData(object):
    pass

class GameMenu(object):

    SCALE = 4 # 1:4 scale

    def __init__(self):
        self.text_bg = [ImageCache.add("images/ui/text_back1.png", True)]
        self.player_bg = [ImageCache.add("images/ui/player_back1.png", True)]

        option_button = ImageCache.add("images/ui/button_back.png")
        option_button = scale(option_button,
            [z*GameMenu.SCALE for z in option_button.get_size()])
        button = ImageCache.add("images/menu/button500x120.png")
        button_h = ImageCache.add("images/menu/button_h500x120.png")
        button_p = ImageCache.add("images/menu/button_p500x120.png")
        button_d = ImageCache.add("images/menu/button_d500x120.png")
        players = [player.Player("Player Tester") for i in range(1)]

        self.dungeon = dungeon.Dungeon("test")
        self.party = party.Party(players)
        self.test_monster = None
        self.resolution = view.get_resolution()
        self.current_location = self.dungeon.start
        self.current_location.generate()
        self.event = self.current_location.get_event()

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

        self.display_dialog(self.event)
        self.display_party()
        self.display_options()
        Dragable((100, 100),
                 surface=scale(ImageCache.add("images/item/test_icon.png", True), (16*4, 16*4)),
                 alpha=True,
                 on_release=None)

    def display_options(self):
        button_position = (self.resolution[0]-12*GameMenu.SCALE,
                           5*GameMenu.SCALE)
        OptionsDisplayData.travel = Button(
            button_position,
            on_pressed = self.display_travel,
            t_info = self.option_style,
            b_info = self.option_button_style,
            text = "Travel")

    def display_party(self):
        # Clean up previous dialogs
        PlayerDisplayData.delete()

        # Create new ui for the players
        for i, member in enumerate(self.party.players):
            chosen_back = random.choice(self.player_bg)
            PlayerDisplayData.back.append(Image(
                pos = (6*GameMenu.SCALE+(i*(chosen_back.get_width()+5))*GameMenu.SCALE, self.resolution[1]-(chosen_back.get_height()+5)*GameMenu.SCALE),
                surface = scale(
                    chosen_back, tuple([z * GameMenu.SCALE
                    for z in chosen_back.get_size()])),
                h_anchor = 1,
                v_anchor = 1,
                alpha = True))

            portrait = ImageCache.add(member.portrait, True)
            PlayerDisplayData.portrait.append(Image(
                pos = (6*GameMenu.SCALE+(i*(chosen_back.get_width()+5))*GameMenu.SCALE, self.resolution[1]-(chosen_back.get_height()+5)*GameMenu.SCALE),
                surface = scale(
                    portrait, tuple([z * GameMenu.SCALE
                    for z in portrait.get_size()])),
                h_anchor = 1,
                v_anchor = 1,
                alpha = True))

            PlayerDisplayData.name.append(Text((
                6*GameMenu.SCALE+(i*(chosen_back.get_width()+5))*GameMenu.SCALE, self.resolution[1]-(chosen_back.get_height()+10)*GameMenu.SCALE), self.text_style,
                text=member.name))

            # Create health bar and speed bar
            health = ImageCache.add("images/ui/health.png")
            speed = ImageCache.add("images/ui/speed.png")
            PlayerDisplayData.health.append(Image(
                pos = (43*GameMenu.SCALE+(i*(chosen_back.get_width()+5))*GameMenu.SCALE, self.resolution[1]-(chosen_back.get_height())*GameMenu.SCALE),
                surface = scale(health, tuple([z * GameMenu.SCALE
                    for z in health.get_size()])),
                h_anchor = 1,
                v_anchor = 1,
                width = round(health.get_width()*member.current_health/member.health*GameMenu.SCALE),
                height = health.get_height()*GameMenu.SCALE))
            PlayerDisplayData.speed.append(Image(
                pos = (43*GameMenu.SCALE+(i*(chosen_back.get_width()+5))*GameMenu.SCALE, self.resolution[1]-(chosen_back.get_height()-5)*GameMenu.SCALE),
                surface = scale(speed, tuple([z * GameMenu.SCALE
                    for z in speed.get_size()])),
                h_anchor = 1,
                v_anchor = 1,
                width = round(speed.get_width()*member.action/member.action_max*GameMenu.SCALE),
                height = speed.get_height()*GameMenu.SCALE))

    def display_travel(self):
        # Clean up previous dialog if any
        if TravelDisplayData.body:
            TravelDisplayData.delete()
            return

        # Create new back
        chosen_back = random.choice(self.text_bg)
        position = (6*GameMenu.SCALE,
                    10*GameMenu.SCALE)
        TravelDisplayData.back = Image(
            position,
            surface = scale(chosen_back, tuple([z * GameMenu.SCALE for z in chosen_back.get_size()])),
            h_anchor = 1,
            v_anchor = 1,
            alpha = True)

        # Create new dialog
        TravelDisplayData.title = Text((6*GameMenu.SCALE, 10*GameMenu.SCALE),
                                        t_info=self.title_style,
                                        text="Travel")
        TravelDisplayData.body = Text((10*GameMenu.SCALE, 15*GameMenu.SCALE),
                                       t_info=self.text_style,
                                       text="You are traveling...")
        displacement = TravelDisplayData.body.get_size()[1]+19*GameMenu.SCALE
        choices = self.current_location.get_neighbours()
        for i, choice in enumerate(choices):
            button_func = partial(self.travel, choice)
            TravelDisplayData.choices.append(Button(
                (10*GameMenu.SCALE, displacement),
                on_pressed=button_func,
                t_info=copy.copy(self.text_style),
                b_info=copy.copy(self.button_style),
                text="%d. %s"%(i+1, choice.loc_type)))
            displacement += TravelDisplayData.choices[-1].get_size()[1]+1*GameMenu.SCALE

    def travel(self, location):
        self.current_location = location
        self.current_location.generate()
        TravelDisplayData.delete()
        self.event = self.current_location.get_event()
        self.display_dialog(self.event)

    def display_dialog(self, dialog):
        # Clean up previous dialog if any
        self.event = dialog
        DialogDisplayData.delete()

        #there is no more dialog
        if not dialog:
            return

        assert not DialogDisplayData.choices

        # Create new back
        chosen_back = random.choice(self.text_bg)
        position = (6*GameMenu.SCALE,
                    10*GameMenu.SCALE)
        DialogDisplayData.back = Image(
            pos = position,
            surface = scale(chosen_back, tuple([z * GameMenu.SCALE for z in chosen_back.get_size()])),
            h_anchor = 1,
            v_anchor = 1,
            alpha = True)

        # Create new dialog
        DialogDisplayData.title = Text((6*GameMenu.SCALE, 10*GameMenu.SCALE),
                          self.title_style,
                          text=self.current_location.get_event_name().title())
        DialogDisplayData.body = Text((10*GameMenu.SCALE, 15*GameMenu.SCALE),
                          self.text_style,
                          text=self.event.body)
        displacement = DialogDisplayData.body.get_size()[1]+19*GameMenu.SCALE
        choices = self.event.get_choices(self.party)
        for i, choice in enumerate(choices):
            button_func = partial(self.display_dialog,
                                  self.event.make_choice(choice))
            DialogDisplayData.choices.append(Button(
                (10*GameMenu.SCALE, displacement), True,
                copy.copy(self.text_style), copy.copy(self.button_style),
                on_pressed=button_func, text="%d. %s"%(i+1, choice)))
            displacement += DialogDisplayData.choices[-1].get_size()[1]+1*GameMenu.SCALE
        if not choices:
            DialogDisplayData.choices.append(Button(
                (10*GameMenu.SCALE, displacement), True,
                copy.copy(self.text_style), copy.copy(self.button_style),
                on_pressed=self.close_dialog,
                text="Next"))

    def close_dialog(self):
        DialogDisplayData.delete()
        if self.event.action:
            self.handle_action(self.event.action)

    def display_loot(self, items, gold):
        #Clean up
        LootDisplayData.delete()

        # Create new back
        tmp_surface = Surface((77, 115), SRCALPHA)
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
        back_position = (self.resolution[0]/2,
                         10*GameMenu.SCALE)
        title_position = (self.resolution[0]/2,
                          10*GameMenu.SCALE)
        button_position = ((self.resolution[0]/2,
                          (displacement+13)*GameMenu.SCALE))

        LootDisplayData.back = Image(
            pos = back_position,
            surface = scale(chosen_back, tuple([z * GameMenu.SCALE for z in chosen_back.get_size()])),
            h_anchor = 0,
            v_anchor = 1,
            alpha = True)

        LootDisplayData.title = Text(
            title_position,
            t_info=self.loot_style,
            text="Treasure")
        displacement = 20*GameMenu.SCALE
        if gold:
            title_position = (self.resolution[0]/2,
                              displacement)
            LootDisplayData.gold = Text(
                title_position,
                t_info=self.loot_style,
                text="Gold - %dg + (%dg)"%(self.party.gold-gold, gold))

        LootDisplayData.close = Button(
                button_position,
                on_pressed=LootDisplayData.delete,
                t_info=copy.copy(self.button_title_style),
                b_info=copy.copy(self.large_button_style),
                text="CLOSE")

    def display_battle(self):
        pass

    def handle_action(self, action):
        key = action.split(" ")[0]
        args = []
        if len(action) > 1:
            args = action.split(" ")[1:]

        gold = 0
        items = [1,2,3]
        if key == "battle":
            if args:
                pass
            else:
                pass
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
            pass
        elif key == "alter":
            pass

        if gold > 0 or items:
            self.display_loot(items, gold)