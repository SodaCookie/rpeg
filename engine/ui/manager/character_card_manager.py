# When we grab an item from the slot, we literally need
# to make a new slot because of how rendering works
# on_click could redraw the slot?

from functools import partial

import pygame

from engine.ui.core.manager import Manager
from engine.ui.core.bindable import Bindable
from engine.ui.core.renderable import Renderable
from engine.ui.core.zone import Zone

from engine.ui.element.window import Window
from engine.ui.element.text import Text
from engine.ui.element.image import Image
from engine.ui.element.bar import Bar
from engine.ui.element.slot import Slot

from engine.game.item.item import Item
from engine.game.move.move import Move

class CharacterCardManager(Manager):
    """Manages the rendering of the character card ui and all
    relevant variables and updates (inventory, moves, etc.)"""


    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.scale = 3
        self.cur_plyr = None
        self.win = Window(400, 400, self.x, self.y)
        self.plyr_img = None
        self.plyr_name = None
        self.plyr_hlth = None
        self.plyr_stats = None
        self.plyr_eqp = []
        self.ply_mv = []
        self.ply_inv = []
        # Ensure code doesn't try to render None or will crash

    def update(self, game):
        # add another condition so doesn't update unnecessarily
        # like during battles
        # only updates renderables when selected player changed
        if game.selected_player != self.cur_plyr and not game.encounter and \
                not game.current_dialog and game.focus_window != "travel":
            # update player
            self.cur_plyr = game.selected_player

            # update image
            img = pygame.image.load(self.cur_plyr.portrait)
            scl_img = pygame.transform.scale(img, (img.get_width()*self.scale, img.get_height()*self.scale))
            self.plyr_img = Image(scl_img, self.x+70-scl_img.get_width()//2, self.y+24)

            # update name
            self.plyr_name = Text(self.cur_plyr.name, 22, 0, self.y+10)
            self.plyr_name.x = self.x+70-self.plyr_name.surface.get_width()//2

            # update health bar
            self.plyr_hlth = Bar(100, 5, (116, 154, 104), self.x+20, self.plyr_img.y+self.plyr_img.surface.get_height()+10)
            self.plyr_action = Bar(100, 5, (212, 196, 148), self.x+20, self.plyr_img.y+self.plyr_img.surface.get_height()+20)

            self.plyr_hlth.percent = 100*self.cur_plyr.get_cur_health()/self.cur_plyr.get_stat("health")
            # String for stat types
            stat_types = "Stats:\n"
            stat_types += ("Attack: \n")
            stat_types += ("Defense: \n")
            stat_types += ("Magic: \n")
            stat_types += ("Health: \n")
            stat_types += ("Resist: \n")
            # String for stat values
            stat_values = "\n"
            stat_values += str(self.cur_plyr.get_stat("attack")) + "\n"
            stat_values += str(self.cur_plyr.get_stat("defense")) + "\n"
            stat_values += str(self.cur_plyr.get_stat("magic")) + "\n"
            stat_values += str(self.cur_plyr.get_stat("health")) + "\n"
            stat_values += str(self.cur_plyr.get_stat("resist")) + "\n"
            self.plyr_stat_types = Text(stat_types, 18, self.x+20, self.y+164,
                width=100, justify=Text.LEFT)
            self.plyr_stat_values = Text(stat_values, 18, self.x+20,
                self.y+164, width=100, justify=Text.RIGHT)

            # update equipment
            self.plyr_eqp = []
            i=0
            # makes a grid, need to add header elements for each slot
            for key, itm in self.cur_plyr.equipment.items():
                self.plyr_eqp.append(Slot(itm, Item, self.x+(64*(i%4))+150, self.y+(100*(i//4))+15, self.cur_plyr.equipment, key))
                i+=1
            # limited to 4 moves only at the moment, need to extend
            self.plyr_mv = []
            for i in range(0,4):
                if i < len(self.cur_plyr.moves):
                    self.plyr_mv.append(Slot(self.cur_plyr.moves[i], Move,
                        self.x+(64*i)+148, self.y+220, self.cur_plyr.moves, i))
                else:
                    self.plyr_mv.append(Slot(None, Move, self.x+(64*i)+148, self.y+220))
            # update inventory
            self.plyr_inv = []
            i=0
            for i, itm in enumerate(self.cur_plyr.inventory):
                self.plyr_eqp.append(Slot(itm, Item, self.x+(64*i)+148,
                    self.y+300, self.cur_plyr.inventory, i))
                i+=1
            # create new renderables list
            self.renderables = []
            self.renderables.append(self.win)
            self.renderables.append(self.plyr_img)
            self.renderables.append(self.plyr_name)
            self.renderables.append(self.plyr_stat_types)
            self.renderables.append(self.plyr_stat_values)
            self.renderables.append(self.plyr_hlth)
            self.renderables.append(self.plyr_action)
            self.renderables.extend(self.plyr_eqp)
            self.renderables.extend(self.plyr_mv)
            # Bind all slots to zones
            self.zones = []
            for slot in self.plyr_eqp:
                on_click = partial(slot.on_click, slot)
                off_click = partial(slot.off_click, slot)
                zone = Zone((slot.x, slot.y, slot.surface.get_width(), slot.surface.get_height()), on_click, None, None, off_click)
                slot.bind(zone)
                self.zones.append(zone)
        # Need to run update functions of the zones
        super().update(game)

    def render(self, surface, game):
        # add conditions so that only renders outside of battles
        if game.selected_player and not game.encounter and \
                not game.current_dialog and game.focus_window != "travel":
            super().render(surface, game)