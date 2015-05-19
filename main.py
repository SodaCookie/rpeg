import pygame
import effects
import monster
import player
import item
import moves



def button_pressed(button, mouse_pos):
    global buttons
    for btn in buttons:
        btn.press(button, mouse_pos)

def render_view():
    global screen, renderables

    screen.fill((255, 255, 255))
    for obj in renderables:
        obj.draw(screen)
        
    pygame.display.flip()



if __name__ == "__main__":
    pygame.init()

    resolution = (800,600)
    screen = pygame.display.set_mode(resolution)

    """
    UI variables

    The view consists of renderables
    The controllers consist of text_inputs and buttons
    This file implements model view and controller TROLOLOLOLOLOL
    """
    renderables = []
    text_inputs = []
    buttons = []

    running = True
    while running:
        for evnt in pygame.event.get():
            if evnt.type == pygame.QUIT:
                running = False

            if evnt.type == pygame.KEYDOWN:
                #text_input(evnt.key)
                pass

            if evnt.type == pygame.MOUSEBUTTONDOWN:
                button_pressed(evnt.button, pygame.mouse.get_pos())

        render_view()
        pygame.time.wait(30)

    pygame.display.quit()
    pygame.quit()