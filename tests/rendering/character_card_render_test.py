import pygame

from engine.ui.manager.mouse_hover_manager import MouseHoverManager
from engine.ui.manager.character_card_manager import CharacterCardManager
from engine.game.player.player import Player
from engine.ui.manager.party_manager import PartyManager
from engine.game.item.item import Item
from engine.game.move.built_moves import *
from engine.game.move.move import Move

class MockGame():
    selected_player = None
    selected_move = None
    mouse_x = 0
    mouse_y = 0
    # Add some math to determine?
    hover_x = -25
    hover_y = -25
    mouse_button = (0, 0, 0)
    party = []
    encounter = []
    current_dialog = None
    focus_window = None

    # mhm
    current_hover = None
    current_object = None
    current_slot = None

# Initialize game and managers
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

mock = MockGame()

mhm = MouseHoverManager()
pm = PartyManager()
ccm = CharacterCardManager(20, 15)

mock.party = [Player("Michael"), Player("Eric"), Player("Peter"), Player("Russel")]

mock.party[0].equipment["hand1"] = Item(rarity="legendary", floor=5)
mock.party[0].add_move(punch)
mock.party[1].equipment["body"] = Item(rarity="legendary", floor=5)

running = True

# game loop
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False


    mock.mouse_x, mock.mouse_y = pygame.mouse.get_pos()
    mock.mouse_button = pygame.mouse.get_pressed()
    pm.update(mock)
    ccm.update(mock)
    mhm.update(mock)
    screen.fill((0, 0, 0))
    pm.render(screen, mock)
    ccm.render(screen, mock)
    mhm.render(screen, mock)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()