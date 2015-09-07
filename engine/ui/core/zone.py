"""Defines the Zone class"""
import pygame

class Zone(object):
    """Zone object defines clickable zones on the screen that can
    execute events (functions). It is not responsible for the rendering
    of the elements on the screen."""

    NEUTRAL = 0
    HOVERED = 1
    CLICKED = 2

    def __init__(self, rect, on_click, on_hover=None, off_hover=None):
        """Takes a pygame rect or any tuple equivalents and a on_click
        the rect describes where the zone is on the screen, and the on_click
        is the function that is given a game object on click.
        on_hover and off hover have also been defined"""
        super(Zone, self).__init__()
        self.rect = pygame.Rect(rect)
        self.on_click = on_click
        self.on_hover = on_hover
        self.off_hover = off_hover
        self.state = Zone.NEUTRAL

    def update(self, game):
        """Takes the game object and figures out the state for the zone"""
        # if previously clicked and button is no longer clicked we call
        # on click
        if self.rect.collidepoint(game.mouse_x, game.mouse_y):
            if self.state == Zone.NEUTRAL:
                if self.on_hover:
                    self.on_hover(game) # the casts on hovered
            state = Zone.HOVERED
            if game.mouse_button[0]: # FIX:
                                     # hovered with clicked makes clicked...
                state = Zone.CLICKED
            elif self.state == Zone.CLICKED:
                # this is where we run the on_click
                self.on_click(game)
        else:
            if self.state != Zone.NEUTRAL:
                if self.off_hover: # off hover
                    self.off_hover(game)
            state = Zone.NEUTRAL
        self.state = state