import pygame


class BattleController(object):
    """Defines an object to be updated per battle loop"""
    battle_controllers = []
    delta_time = pygame.time.get_ticks()

    @staticmethod
    def _handle_battle():
        delta = pygame.time.get_ticks() - BattleController.delta_time
        for controller in BattleController.battle_controllers:
            controller.handle_battle(delta/1000)
        BattleController.delta_time = pygame.time.get_ticks()

    @staticmethod
    def _start_battle():
        BattleController.delta_time = pygame.time.get_ticks()
        for controller in BattleController.battle_controllers:
            controller.handle_start_battle()

    @staticmethod
    def _end_battle():
        for controller in BattleController.battle_controllers:
            controller.handle_end_battle()

    def __init__(self):
        BattleController.battle_controllers.append(self)

    def delete(self):
        BattleController.battle_controllers.remove(self)

    def handle_battle(self, delta): # in seconds
        pass

    def handle_start_battle(self):
        pass

    def handle_end_battle(self):
        pass