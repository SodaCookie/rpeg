import pygame

import engine.ui.manager.character_card_manager as character_card_manager
import engine.game.player.player as player
import engine.ui.manager.party_manager as party_manager
import engine.game.item.item as item

class MockGame():
    selected_player = None
    selected_move = None
    mouse_x = 0
    mouse_y = 0
    mouse_button = (0, 0, 0)
    party = []

# Initialize game and managers
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

mock = MockGame()

pm = party_manager.PartyManager()
ccm = character_card_manager.CharacterCardManager(20, 15)

mock.party = [player.Player("Michael"), player.Player("Eric"), player.Player("Peter"), player.Player("Russel")]

mock.party[0].equipment["hand1"] = item.Item(rarity="legendary", floor=5)
mock.party[1].equipment["body"] = item.Item(rarity="legendary", floor=5)


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
    screen.fill((0, 0, 0))
    pm.render(screen, mock)
    ccm.render(screen, mock)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()