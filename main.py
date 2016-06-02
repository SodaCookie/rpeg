#!python3.5

from engine.main_game import Game
from engine.game.game_system import GameSystem
from engine.game.battle_system import BattleSystem
from engine.ui.ui_system import UISystem
from engine.sound.sound_system import SoundSystem

game = Game()
# attach systems
game.add_system(GameSystem(game))
game.add_system(BattleSystem(game))
game.add_system(UISystem(game))
game.add_system(SoundSystem(game))

game.run()