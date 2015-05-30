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
import objects.shop as shop

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


class GameMenu(object):

    SCALE = 4 # 1:4 scale
    POWER_PER_LEVEL = 100

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
        players = [player.Player("Player Tester") for i in range(4)]

        self.level = 1
        self.power = self.level*GameMenu.POWER_PER_LEVEL
        self.dungeon = dungeon.Dungeon(self.level)
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

        self.single_renderables = {} # add to single_renderables to control
                                     # small elements on the screen
        self.create_group("event", (6*GameMenu.SCALE, 10*GameMenu.SCALE))
        self.create_group("option", (self.resolution[0]-7*GameMenu.SCALE,
                                     5*GameMenu.SCALE))
        self.create_group("party", (0, self.resolution[1]))
        self.create_group("loot", (self.resolution[0]//2, 0))
        self.create_group("travel", (6*GameMenu.SCALE, 10*GameMenu.SCALE))
        self.create_group("shop", (self.resolution[0]//2, 10*GameMenu.SCALE),
            ImageCache.add("images/ui/shop_back.png"), h_anchor=0, v_anchor=1)
        self.render_event(self.event)
        self.render_option()
        self.render_party()

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
            chosen_back = scale(chosen_back, tuple([z*GameMenu.SCALE for z in
                                chosen_back.get_size()]))
            chosen_back.blit(health, (37*GameMenu.SCALE, 5*GameMenu.SCALE),
                (0, 0, round(health.get_width()*member.current_health/
                member.health*GameMenu.SCALE), health.get_height()))
            chosen_back.blit(speed, (37*GameMenu.SCALE, 10*GameMenu.SCALE),
                (0, 0, round(speed.get_width()*member.action/member.action_max*
                GameMenu.SCALE), speed.get_height()))

            Group.party.add(Image(
                pos = (6*GameMenu.SCALE+i*(chosen_back.get_width()+5*GameMenu.SCALE), -5*GameMenu.SCALE),
                surface = chosen_back,
                h_anchor = 1,
                v_anchor = -1,
                alpha = True))

            Group.party.add(Text((
                6*GameMenu.SCALE+i*chosen_back.get_width()+i*5*GameMenu.SCALE, -chosen_back.get_height()-10*GameMenu.SCALE), self.text_style,
                text=member.name))

        Group.party.display()

    def render_travel(self):
        # Clean up previous dialog if any
        Group.travel.delete()

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
                on_pressed=self.close_dialog,
                text="Next"))
        Group.event.display()

    def render_shop(self, shop):

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
                             on_pressed=Group.shop.delete,
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
                v_anchor=1))
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

    def close_dialog(self):
        Group.event.delete()
        if self.event.action:
            self.handle_action(self.event.action)

    def render_loot(self, items, gold):
        #Clean up
        Group.loot.delete()

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
                on_pressed=Group.loot.delete,
                t_info=copy.copy(self.button_title_style),
                b_info=copy.copy(self.large_button_style),
                text="CLOSE"))

        Group.loot.display()

    def display_battle(self):
        pass

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
            s = shop.Shop(self.power, *args)
            self.render_shop(s)
        elif key == "alter":
            pass

        if gold > 0 or items:
            self.render_loot(items, gold)