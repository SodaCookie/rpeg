import random
from functools import partial

from pygame.transform import scale
from pygame import USEREVENT

from classes.rendering.render_group import RenderGroup
from classes.rendering.button import Button, ButtonInfo
from classes.rendering.image import Image
from classes.rendering.text import Text, TextInfo
from classes.image_cache import ImageCache
import classes.rendering.view as view
import classes.controller as controller

class EventMenu(RenderGroup):

    def __init__(self, location, party, game_menu):
        super().__init__("event", (6*view.SCALE, 10*view.SCALE))
        self.event_bg = [ImageCache.add("images/ui/text_back1.png", True)]
        self.location = location
        self.party = party
        self.game_menu = game_menu
        self.event = location.get_event()

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

        self.render(self.event)

    def update(self, event):
        self.delete()
        self.render(event)
        self.display()

    def render(self, dialog):
        self.event = dialog
        #there is no more dialog
        if not dialog:
            return

        # Create new back
        chosen_back = random.choice(self.event_bg)
        self.add(Image(
            pos = (0, 0),
            surface = scale(chosen_back, tuple([z * view.SCALE for z in chosen_back.get_size()])),
            h_anchor = 1,
            v_anchor = 1,
            alpha = True))

        # Create new dialog
        self.add(Text((view.SCALE, 0),
                    self.title_style,
                    text=self.location.get_event_name().title()))
        body = Text((5*view.SCALE, 5*view.SCALE),
                     self.text_style,
                     text=self.event.body)

        self.add(body)
        displacement = body.get_size()[1]+9*view.SCALE
        choices = self.event.get_choices(self.party)
        for i, choice in enumerate(choices):
            button_func = partial(self.update,
                                  self.event.make_choice(choice))
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

    def close_event(self):
        self.delete()
        if self.event.action:
            self.handle_action(self.event.action)

    def handle_action(self, action):
        key = action.split(" ")[0]
        args = []
        if len(action) > 1:
            args = action.split(" ")[1:]

        if key == "battle":
            if args:
                pass
            pygame.event.post(pygame.event.Event(controller.BATTLEEVENT))
            pygame.time.set_timer(controller.BATTLEEVENT, 30)
            monsters = [monster.Monster(100, random.randint(0,2)) for i in range(3)]
            self.current_battle = battle.Battle(self.party, monsters)
            self.busy = True
            self.render_monster()
            self.render_battle_info()
        elif key == "addgold":
            pass
        elif key == "takegold":
            pass
        elif key == "reward":
            gold = int(args[0])
            items = list(args[1])
            self.game_menu.create_loot(gold, items)
            self.game_menu.display_loot()
        elif key == "shop":
            self.game_menu.create_shop()
            self.game_menu.display_shop()
        elif key == "alter":
            pass