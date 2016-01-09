import pygame

class EventHandler(object):
    """Handles events in the game loop"""

    def __init__(self):
        super(EventHandler, self).__init__()
        self.time = pygame.time.get_ticks() # ms

    def update(self, game):
        """Update is responsible for updating the game loop.
        Only EventHandler has the capacity to exit the game"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        self.time = pygame.time.get_ticks() # ms
        game.mouse_x, game.mouse_y = pygame.mouse.get_pos()
        game.mouse_button = pygame.mouse.get_pressed()
        return True



