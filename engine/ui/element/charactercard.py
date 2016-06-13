"""Defines the character renderer."""
import random

import pygame

from engine.system import Message

from engine.ui.element.abstractbutton import AbstractButton
from engine.ui.element.bar import PercentBar
import engine.ui.draw.frame as frame
import engine.ui.draw.simple as simple

class CharacterCard(AbstractButton):
    """Manager for the character class"""

    def __init__(self, name, x, y, position):
        super().__init__(name, (x, y + 30, 280, 156))
        self.font = pygame.font.Font("assets/fonts/VT323-Regular.ttf",
            20)
        self.set_size(280, 150)
        self.draw_seed = random.randint(0, 100)
        self.x = x
        self.y = y
        self.character = None
        self.position = position
        self.health = PercentBar("player-health", x + 136, y + 36, simple.draw_rect(128, 8, (50, 255, 50)))
        self.action = PercentBar("player-action", x + 136, y + 56, simple.draw_rect(128, 8, (50, 100, 50)))

    def on_hovered(self, game, system):
        system.message("sound", Message("ui",
                "data/sound/menu_select_sfx.wav"))

    def on_clicked(self, game, system):
        system.message("sound", Message("ui",
                "data/sound/click.wav"))

    def on_click(self, game, system):
        # In no encounter state
        if not game.encounter and not game.current_dialogue:
            if game.current_player == self.character:
                system.message("ui", Message("layout", "default"))
                system.message("game", Message("select-player", None))
            else:
                system.message("ui", Message("layout", "character"))
                system.message("game", Message("select-player",
                    self.character))
        # During an encounter
        elif game.encounter:
            if game.current_player:
                if game.current_player.selected_move:
                    if game.current_player.selected_move.is_valid_cast(
                            game.current_player.target,
                            game.party.players,
                            game.encounter):
                        game.current_player = self.character
                    elif game.current_player.selected_move.is_valid_target(
                            game.current_player.target + [self.character],
                            game.party.players,
                            game.encounter):
                        game.current_player.target.append(self.character)
                else:
                    game.current_player = self.character

    def off_click(self, game, system):
        pass

    def render_neutral(self, game):
        surface = pygame.Surface((280, 180), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        if self.character is None:
            surface.blit(simple.draw_text("", self.font, (255, 255, 255), 280,
                True), (0, 0))
            surface.blit(frame.draw_frame(280, 156, seed=self.draw_seed), (0, 24))
        else:
            surface.blit(simple.draw_text(self.character.name, self.font, (255, 255, 255), 280,
                True), (0, 0))
            surface.blit(frame.draw_frame(280, 156, seed=self.draw_seed), (0, 24))
            surface.blit(simple.draw_image(self.character.portrait, 4), (4, 16))
            surface.blit(simple.draw_image("image/ui/player_bar.png", 4), (132, 32))
            surface.blit(simple.draw_image("image/ui/player_bar.png", 4), (132, 52))
        return surface

    def render_hover(self, game):
        surface = pygame.Surface((280, 186), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        if self.character is None:
            surface.blit(simple.draw_text("", self.font, (255, 255, 255), 280,
                True), (0, 0))
            surface.blit(frame.draw_highlight_frame(280, 156,
                (255, 255, 255), seed=self.draw_seed), (0, 24))
        else:
            surface.blit(simple.draw_text(self.character.name, self.font, (255, 255, 255), 280,
                True), (0, 0))
            surface.blit(frame.draw_highlight_frame(280, 156,
                (255, 255, 255), seed=self.draw_seed), (0, 24))
            surface.blit(simple.draw_image(self.character.portrait, 4), (4, 16))
            surface.blit(simple.draw_image("image/ui/player_bar.png", 4), (132, 32))
            surface.blit(simple.draw_image("image/ui/player_bar.png", 4), (132, 52))
        return surface

    def render_clicked(self, game):
        surface = pygame.Surface((280, 186), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        if self.character is None:
            surface.blit(simple.draw_text("", self.font, (255, 255, 0),
                280, True), (0, 0))
            surface.blit(frame.draw_highlight_frame(280, 156,
                (255, 255, 0), seed=self.draw_seed), (0, 24))
        else:
            surface.blit(simple.draw_text(self.character.name, self.font, (255, 255, 0),
                280, True), (0, 0))
            surface.blit(frame.draw_highlight_frame(280, 156,
                (255, 255, 0), seed=self.draw_seed), (0, 24))
            surface.blit(simple.draw_image(self.character.portrait, 4), (4, 16))
            surface.blit(simple.draw_image("image/ui/player_bar.png", 4), (132, 32))
            surface.blit(simple.draw_image("image/ui/player_bar.png", 4), (132, 52))
        return surface

    def update(self, game, system):
        self.health.set_percent(self.character.get_cur_health()/ \
            self.character.get_stat("health"))
        self.action.percent(self.character.action/ \
            self.character.get_stat("action"))

    def render(self, surface, game, system):
        if game.party.get_player(self.position) != self.character:
            self.set_dirty(True)
            self.character = game.party.get_player(self.position)
        if self.character is not None:
            super().render(surface, game, system)
            self.health.set_percent(self.character.get_cur_health() / self.character.get_stat("health"))
            self.action.set_percent(self.character.get_cur_action() / self.character.get_stat("action"))
            self.health.render(surface, game, system)
            self.action.render(surface, game, system)
