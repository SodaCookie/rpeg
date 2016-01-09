import pygame


class BattleController(object):
    """Defines an object to be updated per battle loop"""
    battle_controllers = []
    delta_time = pygame.time.get_ticks()

    @staticmethod
    def _handle_battle():
        """Called per iteration of battle loop. Subsequently calls
        each handle_battle function in its list of controllers"""
        delta = pygame.time.get_ticks() - BattleController.delta_time
        for controller in BattleController.battle_controllers:
            controller.handle_battle(delta/1000)
        BattleController.delta_time = pygame.time.get_ticks()

    @staticmethod
    def _start_battle():
        """Called at the start of a battle. Subsequently calls each
        start_battle function in its list of controllers"""
        BattleController.delta_time = pygame.time.get_ticks()
        for controller in BattleController.battle_controllers:
            controller.handle_start_battle()

    @staticmethod
    def _end_battle():
        """Called at the end of a battle. Subsequently calls each
        end_battle function in its list of controllers"""
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