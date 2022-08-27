import pygame
pygame.init()
background = pygame.display.set_mode((400,400))
clock = pygame.time.Clock()
#backgroundPicture = pygame.image.load('Background1.png').convert()
square = pygame.Surface((20,20))
square.fill((255,0,0))
press = pygame.event.get
width = 100
height = 100
left = 0
right = 0
up = 0
down = 0
while True:
    if left:
        width -= 1
    elif right:
        width += 1
    elif up:
        height -= 1
    elif down:
        height += 1
    background.fill(0)
    background.blit(square, (width,height))
    if pygame.event.get(pygame.QUIT):
        break
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                right = 1
            if event.key == pygame.K_LEFT:
                left = 1
            if event.key == pygame.K_UP:
                up = 1
            if event.key == pygame.K_DOWN:
                down = 1
        if event.type == pygame.KEYUP:
            left = 0
            right = 0
            up = 0
            down = 0
    clock.tick(60)
    pygame.display.update()
pygame.quit()

