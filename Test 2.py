import pygame
pygame.init()

game_window = pygame.display.set_mode((400,400))
font = pygame.font.SysFont('Tahoma', 60, True, False)
font = pygame.font.Font('freesansbold.ttf', 48)
text = font.render('Hello world', True, (255, 255, 255))
game_window.blit(text, (100, 100))

while True:
    pygame.init()
    if pygame.event.get(pygame.QUIT):
        break
    pygame.display.update()

pygame.quit()
