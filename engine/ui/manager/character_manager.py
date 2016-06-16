# When we grab an item from the slot, we literally need
# to make a new slot because of how rendering works
# on_click could redraw the slot?

import pygame

from engine.system import Message

from engine.ui.draw.simple import draw_rect
from engine.ui.core.manager import Manager
import engine.ui.element as element

class CharacterManager(Manager):
    """Manages the rendering of the character card ui and all
    relevant variables and updates (inventory, moves, etc.)"""

    _stat_text = \
        "Attack: \n" + \
        "Defense: \n" + \
        "Magic: \n" + \
        "Health: \n" + \
        "Resist: \n" + \
        "Action: \n"

    def __init__(self, x, y, width, height):
        super().__init__("character", x, y)

        self.character = None
        self.name_element = element.Text("name", x + 16, y + 188, "",
            24, width=132)
        self.image_element = element.Image("portrait", x + 36, y,
            draw_rect(144, 140, (255, 255, 255)))
        self.stats_element = element.Text("stats", x + 16, y + 216,
            "", 18, width=132, justify="right")
        self.health = element.PercentBar("player-health", x + 20, y + 128,
            draw_rect(128, 8, (50, 255, 50)))
        self.health_text = element.Text("health-text", x + 20, y + 138, "",
            16, width=132, justify="right")
        self.action = element.PercentBar("player-action", x + 20, y + 162,
            draw_rect(128, 8, (50, 100, 50)))
        self.action_text = element.Text("action-text", x + 20, y + 172, "",
            16, width=132, justify="right")

        self.add_renderable(element.Frame("frame", x, y, width,
            height))
        self.add_renderable(self.health)
        self.add_renderable(self.health_text)
        self.add_renderable(self.action)
        self.add_renderable(self.action_text)
        self.add_renderable(self.name_element)
        self.add_renderable(self.image_element)
        self.add_renderable(self.stats_element)
        self.add_renderable(element.Text("health-btext", x + 20, y + 138,
            "Health:", 16, width=132, justify="left"))
        self.add_renderable(element.Text("action-btext", x + 20, y + 172,
            "Action:", 16, width=132, justify="left"))
        self.add_renderable(element.Text("stat-text", x + 16, y + 216,
            self._stat_text, 18, width=132))
        self.add_renderable(element.Image("health-border", x + 16, y + 124,
            "image/ui/player_bar.png", 4))
        self.add_renderable(element.Image("action-border", x + 16, y + 158,
            "image/ui/player_bar.png", 4))

        # Level up
        self.shard_element = element.Text("required-shard", x + 280, y + 36,
            "", 20, width=200)
        self.add_renderable(self.shard_element)
        self.add_renderable(element.Text("required-text", x + 280, y + 16,
            "Shards Required: ", 20, width=200))
        self.add_renderable(element.Button("level-up",
            self.level_up,
            text = "Level Up",
            size = 20,
            x = x + 168,
            y = y + 16,
            width = 100,
            height = 50))

        # Equipment Slots
        self.equipment_elements = {}
        equipment_x = x + 420
        equipment_y = y + 16
        # Hand
        self.add_renderable(element.Text("text-hand1", equipment_x,
            equipment_y + 56, "Hand", 16, width=54, justify="center"))
        self.equipment_elements["hand1"] = element.ItemSlot("equipment-hand1",
            equipment_x, equipment_y, "hand", None, self.update_stats())

        # Hand
        self.add_renderable(element.Text("text-hand2", equipment_x + 60,
            equipment_y + 56, "Hand", 16, width=54, justify="center"))
        self.equipment_elements["hand2"] = element.ItemSlot("equipment-hand2",
            equipment_x + 60, equipment_y, "hand", None, self.update_stats())

        # Body
        self.add_renderable(element.Text("text-body", equipment_x,
            equipment_y + 136, "Body", 16, width=54, justify="center"))
        self.equipment_elements["body"] = element.ItemSlot("equipment-body",
            equipment_x, equipment_y + 80, "body", None, self.update_stats())

        # Legs
        self.add_renderable(element.Text("text-legs", equipment_x + 60,
            equipment_y + 136, "Legs", 16, width=54, justify="center"))
        self.equipment_elements["legs"] = element.ItemSlot("equipment-legs",
            equipment_x + 60, equipment_y + 80, "legs", None,
            self.update_stats())

        # Feet
        self.add_renderable(element.Text("text-feet", equipment_x,
            equipment_y + 216, "Feet", 16, width=54, justify="center"))
        self.equipment_elements["feet"] = element.ItemSlot("equipment-feet",
            equipment_x, equipment_y + 160, "feet", None, self.update_stats())

        # Head
        self.add_renderable(element.Text("text-head", equipment_x + 60,
            equipment_y + 216, "Head", 16, width=54, justify="center"))
        self.equipment_elements["head"] = element.ItemSlot("equipment-head",
            equipment_x + 60, equipment_y + 160, "head", None,
            self.update_stats())

        # Extra
        self.add_renderable(element.Text("text-extra1", equipment_x,
            equipment_y + 296, "Extra", 16, width=54, justify="center"))
        self.equipment_elements["extra1"] = element.ItemSlot(
            "equipment-extra1", equipment_x, equipment_y + 240, "extra", None, self.update_stats())

        # Extra
        self.add_renderable(element.Text("text-extra2", equipment_x + 60,
            equipment_y + 296, "Extra", 16, width=54, justify="center"))
        self.equipment_elements["extra2"] = element.ItemSlot(
            "equipment-extra2", equipment_x + 60, equipment_y + 240, "extra",
            None, self.update_stats())

        for elem in self.equipment_elements.values():
            self.add_renderable(elem)

        # Move slots
        move_x = x + 168
        move_y = y + 152
        self.move_elements = []
        self.add_renderable(element.Text("moves-text", move_x + 4, move_y - 32,
            "Abilities", 24, width=132, justify="left"))
        for i in range(12):
            item_element = element.MoveSlot("move-slot-%d" % i,
                move_x + (i % 4) * 60, move_y + (i // 4) * 60, None)
            self.move_elements.append(item_element)
            self.add_renderable(item_element)

    def set_player(self, player):
        self.name_element.set_text(player.name)
        self.image_element.set_surface(player.portrait, 3)
        self.shard_element.set_text(str(player.get_level_required_shard()))

        # Set stats
        stat_values = ""
        stat_values += str(player.get_stat("attack")) + "\n"
        stat_values += str(player.get_stat("defense")) + "\n"
        stat_values += str(player.get_stat("magic")) + "\n"
        stat_values += str(player.get_stat("health")) + "\n"
        stat_values += str(player.get_stat("resist")) + "\n"
        stat_values += str(player.get_stat("action"))
        self.stats_element.set_text(stat_values)

        # Update equipment
        for key, elem in self.equipment_elements.items():
            elem.set_new_address((player.equipment, key))

        # Update moves
        for i in range(len(self.move_elements)):
            if i < len(player.moves):
                self.move_elements[i].set_new_address((player.moves, i))
            else:
                self.move_elements[i].set_new_address(None)

    def update(self, game, system):
        if game.current_player is not self.character:
            self.set_player(game.current_player)
            self.character = game.current_player

        if self.character is not None:
            self.health.set_percent(self.character.get_cur_health() /
                self.character.get_stat("health"))
            self.action.set_percent(self.character.get_cur_action() /
                self.character.get_stat("action"))
            self.health_text.set_text("%d/%d" % \
                (self.character.get_cur_health(),
                 self.character.get_stat("health")))
            self.action_text.set_text("%d/%d" % \
                (self.character.get_cur_action(),
                 self.character.get_stat("action")))

    def update_stats(self):
        def on_change(game, system):
            stat_values = ""
            stat_values += str(self.character.get_stat("attack")) + "\n"
            stat_values += str(self.character.get_stat("defense")) + "\n"
            stat_values += str(self.character.get_stat("magic")) + "\n"
            stat_values += str(self.character.get_stat("health")) + "\n"
            stat_values += str(self.character.get_stat("resist")) + "\n"
            stat_values += str(self.character.get_stat("action"))
            self.stats_element.set_text(stat_values)
        return on_change

    def level_up(self, game, system):
        if game.party.shards >= self.character.get_level_required_shard():
            system.message("ui", Message("push-bg", (50, 50, 50)))
            system.message("ui", Message("layout", "level"))
            system.message("game", Message("shard",
                -self.character.get_level_required_shard()))
            system.message("game", Message("level", self.character))
        else:
            system.message("animation", Message("message", "Insufficient shards to level up", (255, 0, 0)))

    # def update(self, game):
    #     """Updates the the character card manager to reflect changes when called."""
    #     # add another condition so doesn't update unnecessarily
    #     # like during battles
    #     # only updates renderables when selected player changed
    #     if not game.selected_player:
    #         return

    #     if game.selected_player != self.cur_plyr and not game.encounter and \
    #             not game.current_dialogue and game.focus_window != "travel":
    #         # update player
    #         self.cur_plyr = game.selected_player

    #         # update image
    #         img = pygame.image.load(self.cur_plyr.portrait)
    #         scl_img = pygame.transform.scale(img, (img.get_width()*self.scale, img.get_height()*self.scale))
    #         self.plyr_img = Image(scl_img, self.x+70-scl_img.get_width()//2, self.y+24)

    #         # update name
    #         self.plyr_name = Text(self.cur_plyr.name, 22, 0, self.y+10)
    #         self.plyr_name.x = self.x+70-self.plyr_name.surface.get_width()//2

    #         # update health bar
    #         self.plyr_hlth = Bar(100, 5, (116, 154, 104), self.x+20, self.plyr_img.y+self.plyr_img.surface.get_height()+10)
    #         self.plyr_action = Bar(100, 5, (212, 196, 148), self.x+20, self.plyr_img.y+self.plyr_img.surface.get_height()+20)

    #         self.plyr_hlth.percent = 100*self.cur_plyr.get_cur_health()/self.cur_plyr.get_stat("health")
    #         # String for stat types
    #         stat_types = "Stats:\n"
    #         stat_types += ("Attack: \n")
    #         stat_types += ("Defense: \n")
    #         stat_types += ("Magic: \n")
    #         stat_types += ("Health: \n")
    #         stat_types += ("Resist: \n")
    #         # String for stat values
    #         stat_values = "\n"
    #         stat_values += str(self.cur_plyr.get_stat("attack")) + "\n"
    #         stat_values += str(self.cur_plyr.get_stat("defense")) + "\n"
    #         stat_values += str(self.cur_plyr.get_stat("magic")) + "\n"
    #         stat_values += str(self.cur_plyr.get_stat("health")) + "\n"
    #         stat_values += str(self.cur_plyr.get_stat("resist")) + "\n"
    #         self.plyr_stat_types = Text(stat_types, 18, self.x+20, self.y+164,
    #             width=100, justify=Text.LEFT)
    #         self.plyr_stat_values = Text(stat_values, 18, self.x+20,
    #             self.y+164, width=100, justify=Text.RIGHT)

    #         # update equipment
    #         equipment = Text("Equipment", 22, self.x+150, self.y+10)
    #         self.plyr_eqp = []
    #         i = 0
    #         equipment_text = []

    #         # makes a grid, need to add header elements for each slot
    #         for key, itm in self.cur_plyr.equipment.items():
    #             self.plyr_eqp.append(Slot(itm, Item, self.x+(56*(i%4))+150, self.y+(76*(i//4))+40, self.cur_plyr.equipment, key))
    #             text = Text(key, 16, self.x+(56*(i%4))+150, self.y+(76*(i//4))+92)
    #             equipment_text.append(text)
    #             i += 1

    #         # limited to 4 moves only at the moment, need to extend
    #         skill_text = Text("Skills", 22, self.x+150, self.y+192)
    #         self.plyr_mv = []
    #         for i in range(0,12):
    #             if i < len(self.cur_plyr.moves):
    #                 move = self.cur_plyr.moves[i]
    #             else:
    #                 move = None
    #             self.plyr_mv.append(Slot(move, Move, self.x+(56*(i%4))+148, self.y+(56*(i//4)+220), self.cur_plyr.moves, i)) # Can't move moves to this one

    #         # Create level up button
    #         level_up_button = Button("LEVEL UP", 28, self.x+20,
    #             self.y+self.win.height-60, True)

    #         # Create zone for button
    #         level_up_zone = Zone(level_up_button.get_rect(),
    #             on_click = self.on_level_up_click)
    #         level_up_button.bind(level_up_zone)

    #         # Add to renderables
    #         self.renderables = []
    #         self.renderables.append(self.win)
    #         self.renderables.append(self.plyr_img)
    #         self.renderables.append(equipment)
    #         self.renderables.append(self.plyr_name)
    #         self.renderables.append(self.plyr_stat_types)
    #         self.renderables.append(self.plyr_stat_values)
    #         self.renderables.append(self.plyr_hlth)
    #         self.renderables.append(self.plyr_action)
    #         self.renderables.extend(self.plyr_eqp)
    #         self.renderables.extend(self.plyr_mv)
    #         self.renderables.append(skill_text)
    #         self.renderables.extend(equipment_text)
    #         self.renderables.append(level_up_button)
    #         # Bind all slots to zones
    #         self.zones = []
    #         self.zones.append(level_up_zone)
    #         for slot in self.plyr_eqp:
    #             on_click = partial(self.on_item_click, slot)
    #             off_click = partial(self.on_item_off_click, slot)
    #             zone = Zone((slot.x, slot.y, slot.surface.get_width(), slot.surface.get_height()), on_click, None, None, off_click)
    #             slot.bind(zone)
    #             self.zones.append(zone)

    #         for slot in self.plyr_mv:
    #             on_click = partial(slot.on_click, slot,
    #                 self.equip_drag_validator, True)
    #             off_click = partial(slot.off_click, slot,
    #                 self.equip_drop_validator, False)
    #             zone = Zone((slot.x, slot.y, slot.surface.get_width(), slot.surface.get_height()), on_click, None, None, off_click)
    #             slot.bind(zone)
    #             self.zones.append(zone)
    #     # Need to run update functions of the zones
    #     if game.selected_player and not game.encounter:
    #         super().update(game)

    # def update_text(self):
    #     stat_values = "\n"
    #     stat_values += str(self.cur_plyr.get_stat("attack")) + "\n"
    #     stat_values += str(self.cur_plyr.get_stat("defense")) + "\n"
    #     stat_values += str(self.cur_plyr.get_stat("magic")) + "\n"
    #     stat_values += str(self.cur_plyr.get_stat("health")) + "\n"
    #     stat_values += str(self.cur_plyr.get_stat("resist")) + "\n"
    #     self.plyr_stat_values.set_text(stat_values)

    # def on_item_click(self, slot, game):
    #     Slot.on_click(slot, self.equip_drag_validator, False, game)
    #     self.update_text()

    # def on_item_off_click(self, slot, game):
    #     Slot.off_click(slot, self.equip_drop_validator, False, game)
    #     self.update_text()

    # @staticmethod
    # def on_level_up_click(game):
    #     if game.selected_player.can_level_up(game.party.shards):
    #         game.focus_window = "level"
    #         game.selected_player.roll_moves()

    # @staticmethod
    # def equip_drag_validator(slot, game):
    #     return True

    # @staticmethod
    # def equip_drop_validator(slot, game):
    #     return game.current_object.slot in slot.key

    # @staticmethod
    # def move_drag_validator(slot, game):
    #     return not game.encounter

    # @staticmethod
    # def move_drop_validator(slot, game):
    #     return False # I dont wanna deal with you...