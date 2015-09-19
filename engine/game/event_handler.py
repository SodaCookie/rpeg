import pygame

class EventHandler(object):
    """docstring for EventHandler"""

    def __init__(self):
        super(EventHandler, self).__init__()

    def update(self, game):
        """Update is responsible for updating the game loop.
        Only EventHandler has the capacity to exit the game"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        game.mouse_x, game.mouse_y = pygame.mouse.get_pos()
        game.mouse_button = pygame.mouse.get_pressed()
        return True
