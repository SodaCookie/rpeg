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
from engine.ui.element.button import Button

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
        self.win = Window(408, 390, self.x, self.y)
        self.plyr_img = None
        self.plyr_name = None
        self.plyr_hlth = None
        self.plyr_stats = None
        self.plyr_eqp = []
        self.ply_mv = []
        self.ply_inv = []
        # Ensure code doesn't try to render None or will crash

    def update(self, game):
        """Updates the the character card manager to reflect changes when called."""
        # add another condition so doesn't update unnecessarily
        # like during battles
        # only updates renderables when selected player changed
        if not game.selected_player:
            return

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
            equipment = Text("Equipment", 22, self.x+150, self.y+10)
            self.plyr_eqp = []
            i = 0
            equipment_text = []

            # makes a grid, need to add header elements for each slot
            for key, itm in self.cur_plyr.equipment.items():
                self.plyr_eqp.append(Slot(itm, Item, self.x+(56*(i%4))+150, self.y+(76*(i//4))+40, self.cur_plyr.equipment, key))
                text = Text(key, 16, self.x+(56*(i%4))+150, self.y+(76*(i//4))+92)
                equipment_text.append(text)
                i += 1

            # limited to 4 moves only at the moment, need to extend
            skill_text = Text("Skills", 22, self.x+150, self.y+192)
            self.plyr_mv = []
            for i in range(0,12):
                if i < len(self.cur_plyr.moves):
                    move = self.cur_plyr.moves[i]
                else:
                    move = None
                self.plyr_mv.append(Slot(move, Move, self.x+(56*(i%4))+148, self.y+(56*(i//4)+220), self.cur_plyr.moves, i)) # Can't move moves to this one

            # Create level up button
            level_up_button = Button("LEVEL UP", 28, self.x+20,
                self.y+self.win.height-60, True)

            # Create zone for button
            level_up_zone = Zone(level_up_button.get_rect(),
                on_click = self.on_level_up_click)
            level_up_button.bind(level_up_zone)

            # Add to renderables
            self.renderables = []
            self.renderables.append(self.win)
            self.renderables.append(self.plyr_img)
            self.renderables.append(equipment)
            self.renderables.append(self.plyr_name)
            self.renderables.append(self.plyr_stat_types)
            self.renderables.append(self.plyr_stat_values)
            self.renderables.append(self.plyr_hlth)
            self.renderables.append(self.plyr_action)
            self.renderables.extend(self.plyr_eqp)
            self.renderables.extend(self.plyr_mv)
            self.renderables.append(skill_text)
            self.renderables.extend(equipment_text)
            self.renderables.append(level_up_button)
            # Bind all slots to zones
            self.zones = []
            self.zones.append(level_up_zone)
            for slot in self.plyr_eqp:
                on_click = partial(self.on_item_click, slot)
                off_click = partial(self.on_item_off_click, slot)
                zone = Zone((slot.x, slot.y, slot.surface.get_width(), slot.surface.get_height()), on_click, None, None, off_click)
                slot.bind(zone)
                self.zones.append(zone)

            for slot in self.plyr_mv:
                on_click = partial(slot.on_click, slot,
                    self.equip_drag_validator, True)
                off_click = partial(slot.off_click, slot,
                    self.equip_drop_validator, False)
                zone = Zone((slot.x, slot.y, slot.surface.get_width(), slot.surface.get_height()), on_click, None, None, off_click)
                slot.bind(zone)
                self.zones.append(zone)
        # Need to run update functions of the zones
        if game.selected_player and not game.encounter:
            super().update(game)

    def update_text(self):
        stat_values = "\n"
        stat_values += str(self.cur_plyr.get_stat("attack")) + "\n"
        stat_values += str(self.cur_plyr.get_stat("defense")) + "\n"
        stat_values += str(self.cur_plyr.get_stat("magic")) + "\n"
        stat_values += str(self.cur_plyr.get_stat("health")) + "\n"
        stat_values += str(self.cur_plyr.get_stat("resist")) + "\n"
        self.plyr_stat_values.set_text(stat_values)

    def on_item_click(self, slot, game):
        Slot.on_click(slot, self.equip_drag_validator, False, game)
        self.update_text()

    def on_item_off_click(self, slot, game):
        Slot.off_click(slot, self.equip_drop_validator, False, game)
        self.update_text()

    @staticmethod
    def on_level_up_click(game):
        if game.selected_player.can_level_up(game.party.shards):
            game.focus_window = "level"
            game.selected_player.roll_moves()

    @staticmethod
    def equip_drag_validator(slot, game):
        return True

    @staticmethod
    def equip_drop_validator(slot, game):
        return game.current_object.slot in slot.key

    @staticmethod
    def move_drag_validator(slot, game):
        return not game.encounter

    @staticmethod
    def move_drop_validator(slot, game):
        return False # I dont wanna deal with you...

    def render(self, surface, game):
        # add conditions so that only renders outside of battles
        if game.selected_player and not game.encounter and \
                not game.current_dialog and game.focus_window != "travel":
            super().render(surface, game)