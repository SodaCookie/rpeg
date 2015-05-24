from functools import partial
import random
import copy

from pygame.transform import scale

import view
from image_cache import ImageCache
from image import Image
from text import Text, TextInfo
from button import Button, ButtonInfo
import objects.dungeon as dungeon
import objects.party as party
import objects.player as player

class PlayerDisplayData(object):

    def __init__(self):
        self.back = None
        self.portrait = None
        self.name = None

class GameMenu(object):

    SCALE = 4 # 1:4 scale

    def __init__(self):
        self.text_bg = [ImageCache.add("images/ui/text_back1.png", True)]
        self.player_bg = [ImageCache.add("images/ui/player_back1.png", True)]
        button = ImageCache.add("images/menu/button500x120.png")
        button_h = ImageCache.add("images/menu/button_h500x120.png")
        button_p = ImageCache.add("images/menu/button_p500x120.png")
        button_d = ImageCache.add("images/menu/button_d500x120.png")
        self.dungeon = dungeon.Dungeon("test")
        players = [player.Player("Player the Terrible") for i in range(4)]
        self.player_display_data = []
        self.party = party.Party(players)
        self.choices = []
        self.body = None
        self.dungeon.start.generate()
        self.text_style = TextInfo(fontcolor=(255,255,255),
                                   fontsize=16,
                                   alignment=-1,
                                   h_anchor=1,
                                   v_anchor=1,
                                   wrap=True,
                                   width=149*GameMenu.SCALE);
        self.button_style = ButtonInfo(
            500, 14, (255, 255, 255), (255, 255, 0), (0, 128, 0), (0, 0, 0),
            None, None, None, None, h_anchor=1, v_anchor=1);

        self.resolution = view.get_resolution()
        self.event = self.dungeon.start.get_event()
        self.display_dialog(self.event)
        self.display_party()

    def display_party(self):
        # Clean up previous dialogs
        self.close_party()

        # Create new ui for the players
        for i, member in enumerate(self.party.players):
            player_display_data = PlayerDisplayData()
            chosen_back = random.choice(self.player_bg)
            player_display_data.back = Image(
                pos = (
                   6*GameMenu.SCALE+(i*(chosen_back.get_width()+5))*GameMenu.SCALE, self.resolution[1]-(chosen_back.get_height()+5)*GameMenu.SCALE),
                surface = scale(
                    chosen_back, tuple([z * GameMenu.SCALE
                    for z in chosen_back.get_size()])),
                h_anchor = 1,
                v_anchor = 1,
                alpha = True)
            portrait = ImageCache.add(member.portrait, True)

            player_display_data.portrait = Image(
                pos = (
                   6*GameMenu.SCALE+(i*(chosen_back.get_width()+5))*GameMenu.SCALE, self.resolution[1]-(chosen_back.get_height()+5)*GameMenu.SCALE),
                surface = scale(
                    portrait, tuple([z * GameMenu.SCALE
                    for z in portrait.get_size()])),
                h_anchor = 1,
                v_anchor = 1,
                alpha = True)

            player_display_data.text =  Text((
                6*GameMenu.SCALE+(i*(chosen_back.get_width()+5))*GameMenu.SCALE, self.resolution[1]-(chosen_back.get_height()+10)*GameMenu.SCALE), self.text_style,
                member.name)

    def close_party(self):
        if self.player_display_data:
            for player in self.player_display_data:
                player.back.delete()
                player.portrait.delete()
                player.text.delete()

    def display_dialog(self, dialog):
        # Clean up previous dialog if any
        self.event = dialog
        if self.body:
            self.text_back.delete()
            self.body.delete()
            for choice in self.choices:
                choice.delete()
            self.choices = []

        #there is no more dialog
        if not dialog:
            return

        assert not self.choices

        # Create new back
        chosen_back = random.choice(self.text_bg)
        self.text_back = Image(
            pos = (6*GameMenu.SCALE, 5*GameMenu.SCALE),
            surface = scale(chosen_back, tuple([z * GameMenu.SCALE for z in chosen_back.get_size()])),
            h_anchor = 1,
            v_anchor = 1,
            alpha = True)

        # Create new dialog
        self.body = Text((10*GameMenu.SCALE, 10*GameMenu.SCALE),
                          self.text_style,
                          self.event.body)
        choices = self.event.get_choices(self.party)
        for i, choice in enumerate(choices):
            button_func = partial(self.display_dialog,
                                  self.event.make_choice(choice))
            self.choices.append(Button(
                (6*GameMenu.SCALE, 250+i*25), button_func, None,
                copy.copy(self.text_style), copy.copy(self.button_style),
                True, choice))
        if not choices:
            self.choices.append(Button(
                (self.resolution[0]/4, 300), self.close_dialog, None,
                copy.copy(self.text_style), copy.copy(self.button_style),
                True, "Next"))

    def close_dialog(self):
        """Closes dialog and will activate any action pushed from event"""
        self.event = None
        if self.body:
            self.text_back.delete()
            self.body.delete()
            for choice in self.choices:
                choice.delete()
            self.choices = []
