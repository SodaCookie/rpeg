"""Defines the Zone class"""
import pygame

class Zone(object):
    """Zone object defines clickable zones on the screen that can
    execute events (functions). It is not responsible for the rendering
    of the elements on the screen."""

    NEUTRAL = 0
    HOVERED = 1
    CLICKED = 2

    def __init__(self, rect, on_click):
        """Takes a pygame rect or any tuple equivalents and a on_click
        the rect describes where the zone is on the screen, and the on_click
        is the function that is given a game object on click"""
        super(Zone, self).__init__()
        self.rect = pygame.Rect(rect)
        self.on_click = on_click
        self.state = Zone.NEUTRAL

    def update(self, game):
        """Takes the game object and figures out the state for the zone"""
        # if previously clicked and button is no longer clicked we call
        # on click
        state = Zone.NEUTRAL
        if self.rect.collidepoint(game.mouse_x, game.mouse_y):
            state = Zone.HOVERED
            if game.mouse_button[0]:
                state = Zone.CLICKED
            elif self.state == Zone.CLICKED:
                # this is where we run the on_click
                self.on_click(game)
        self.state = state