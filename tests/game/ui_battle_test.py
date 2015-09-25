import pygame

import engine.game.move.built_moves as built_moves
import engine.game.monster.monster as monster
import engine.game.player.player as player
import engine.ui.manager.party_manager as party_manager
import engine.ui.manager.castbar_manager as castbar_manager
import engine.ui.manager.encounter_manager as encounter_manager

class MockGame():
    selected_player = None
    selected_move = None
    selected_target = None
    mouse_x = 0
    mouse_y = 0
    mouse_button = (0, 0, 0)
    party = []
    encounter = []

# Initialize game and managers
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

mock = MockGame()

pm = party_manager.PartyManager()
cbm = castbar_manager.CastBarManager(400)
em = encounter_manager.EncounterManager()

mock.party = [player.Player("Michael"), player.Player("Eric"), player.Player("Peter"), player.Player("Russel")]
mock.encounter = [monster.Monster() for i in range(4)]

mock.party[0].castbar[3] = built_moves.slash
mock.party[1].castbar[0] = built_moves.slash
mock.party[1].castbar[2] = built_moves.magic_bolt
mock.party[2].castbar[4] = built_moves.punch
mock.party[3].castbar[5] = built_moves.magic_blast

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
    cbm.update(mock)
    em.update(mock)
    if mock.selected_move: print(mock.selected_move)
    #once action executed, deselect target and move
    if mock.selected_player and mock.selected_move and mock.selected_target:
        mock.selected_move.cast(mock.selected_target, mock.selected_player, mock.party, mock.encounter)
        print("Player: " + mock.selected_player.name + "   Move: " + mock.selected_move.name
         + "   Target: " + mock.selected_target.name + "   Target Health: " + str(mock.selected_target.get_cur_health()))
        mock.selected_player, mock.selected_move, mock.selected_target = (None, None, None)
    screen.fill((0, 0, 0))
    pm.render(screen, mock)
    cbm.render(screen, mock)
    em.render(screen, mock)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()