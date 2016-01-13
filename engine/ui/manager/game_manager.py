from collections import OrderedDict

from engine.game.dungeon.dungeon import Dungeon
from engine.game.player.player import Player
from engine.game.party.party import Party
from engine.ui.core.manager import Manager
import engine.ui.manager as manager

import engine.game.move.built_moves as mv

class GameManager(Manager):
    """GameManager is responsible for rendering and updating
    all the various gameplay related elements in the game
    it also controls pseudorandom ordering of menu systems
    in the form of the manager list. It is also in charge of macro
    level logic of the rendering of the menus."""

    def __init__(self):
        super(GameManager, self).__init__()
        self.hover = manager.MouseHoverManager()
        self.party = manager.PartyManager()
        self.sidebar = manager.SidebarManager()
        self.encounter = manager.EncounterManager()
        self.castbar = manager.CastBarManager(440)
        self.loot = manager.LootManager(450, 20, 300, 400)
        self.scenario = manager.ScenarioManager(20, 60)
        self.travel = manager.TravelManager(800, 300, 1280//2-800//2, 100)
        self.battle = manager.BattleManager()
        self.shop = None
        self.character = manager.CharacterCardManager(20, 20)
        self.item = None

    def init(self, game, difficulty):
        # May need to shift this functionality
        game.difficulty = difficulty
        game.current_dungeon = Dungeon("catacombs", game.difficulty)
        game.floor_type = game.current_dungeon.level
        game.current_location = game.current_dungeon.start
        game.current_location.generate()
        game.current_dialog = game.current_location.get_event()
        game.focus_window = "scenario"
        game.party = Party([Player("Player "+str(i)) for i in range(3)])
        for player in game.party.players:
            player.add_move(mv.PLAYER_MOVES["healing word"])
            player.add_move(mv.PLAYER_MOVES["attack"])
            player.castbar[0] = player.moves[0] # temp
            player.castbar[1] = player.moves[1] # temp

    def render(self, surface, game):
        super().render(surface, game)
        self.sidebar.render(surface, game)
        self.encounter.render(surface, game)
        self.party.render(surface, game)
        self.character.render(surface, game)
        self.loot.render(surface, game)
        self.castbar.render(surface, game)
        if game.focus_window == "travel":
            self.travel.render(surface, game)
        elif game.focus_window == "shop":
            pass
        elif game.focus_window == "loot":
            pass
        elif game.focus_window == "scenario":
            self.scenario.render(surface, game)
        self.hover.render(surface, game)
        # self.item.render(surface, game)

    def update(self, game):
        super().update(game)
        self.battle.update(game)
        self.sidebar.update(game)
        self.party.update(game)
        self.character.update(game)
        self.castbar.update(game)
        self.encounter.update(game)
        self.loot.update(game)
        if game.focus_window == "travel":
            self.travel.update(game)
        if game.focus_window == "shop":
            pass
        if game.focus_window == "loot":
            pass
        if game.focus_window == "scenario":
            self.scenario.update(game)
        self.hover.update(game)
        # self.item.update(game)