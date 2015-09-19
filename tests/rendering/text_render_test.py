import pygame

from engine.ui.element.text import Text

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
text1 =  Text("Hello World!", 14, 100, 100)
text2 =  Text("Hello World!", 20, 100, 200)
text3 =  Text("Hello World!", 14, 100, 300, (255, 0, 0))
text4 =  Text("Hello World! Word Wrapping with long sentences and some numbers (123) and some symbols ($%^&*)", 14, 100, 400, (255, 255, 255), 200)
text6 =  Text("Hello World! Word Wrapping with long sentences and some numbers (123) and some symbols ($%^&*)\nHello\n\nMore text and what not. Just get some more words on the screen", 14, 300, 200, (255, 255, 255), 200, Text.CENTER)
text5 =  Text("Hello World! Word Wrapping with long sentences and some numbers (123) and some symbols ($%^&*)", 14, 300, 100, (255, 255, 255), 200, Text.RIGHT)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    screen.fill((0, 0, 0))
    text1.render(screen, None)
    text2.render(screen, None)
    text3.render(screen, None)
    text4.render(screen, None)
    text5.render(screen, None)
    text6.render(screen, None)
    clock.tick(60)

pygame.quit()