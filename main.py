import pygame
import time
from pygame.locals import *
# pygame.init starts the code
pygame.init()
# create time
clock = pygame.time.Clock()
# background width and height
backgroundwidth = 1000
backgroundheight = 500
# set background image size
background = pygame.display.set_mode((backgroundwidth,backgroundheight))
# defining variables
tile_size = 50
FPS = 60
main_menu = True
#global gameOver
gameOver = 0
# are we in the main menu
InMainMenu = True
#load images
restartButtonImage = pygame.image.load('Redo Button.png')
ExitButtonImage = pygame.image.load('Exit.png')
HomeButtonImage = pygame.image.load('Home button.png')
class RedoButton():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.click = False #has it been clicked
    def draw_button(self):
        action = False
        pos = pygame.mouse.get_pos() #to get mouse position

        #add in code for checking clicking
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
                action = True
                self.click = True
        if pygame.mouse.get_pressed()[0] == 0:
                self.click = False

        background.blit(self.image, self.rect)
        return action

class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, gameOver):
        dx = 0
        dy = 0
        walkCoolDown = 20

        if gameOver == 0:
            # get keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_UP] and self.jumped == False and self.in_air == False:
                self.Speed = -15
                self.jumped = True
            if key[pygame.K_UP] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1

            #gravity
            self.Speed += 1
            if self.Speed > 10:
                self.Speed = 10
            dy += self.Speed
            #collision checks
            self.in_air = True
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.SpriteWidth, self.SpriteHeight):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.SpriteWidth, self.SpriteHeight):
                    if self.Speed < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.Speed = 0
                    elif self.Speed >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.Speed = 0
                        self.in_air = False
            # checking if player collides with certain objects
            if pygame.sprite.spritecollide(self, AllSpriteList, False):
                gameOver = -1
            if pygame.sprite.spritecollide(self, AllFlagList, False):
                gameOver = 1

            self.rect.x += dx
            self.rect.y += dy

        elif gameOver == -1:
            self.image = self.deadImage
            if self.rect.y > -100:
                self.rect.y -= 3
        background.blit(self.image, self.rect)
        pygame.draw.rect(background, (255, 255, 255), self.rect, 2)
        return gameOver
    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        # load & scale images
        img = pygame.image.load('KrisSprite.png')
        deadImg = pygame.image.load('KrisFallen.png')
        self.image = pygame.transform.scale(img, (50, 100))
        self.deadImage = pygame.transform.scale(deadImg, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.SpriteWidth = self.image.get_width()
        self.SpriteHeight = self.image.get_height()
        self.Speed = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True
class World():
    def __init__(self, data):
        self.tile_list = []
        PlatformerBlock1 = pygame.image.load('PlatformerBlock.png')
        row_index = 0
        # if grid tile = 1 on grid make block
        for row in data:
            column_index = 0
            for tile in row:
                if tile == 1:
                    TruePlatformerBlock1 = pygame.transform.scale(PlatformerBlock1, (tile_size, tile_size))
                    TruePlatformerBlock1_rect = TruePlatformerBlock1.get_rect()
                    TruePlatformerBlock1_rect.x = column_index*tile_size
                    TruePlatformerBlock1_rect.y = row_index*tile_size
                    tile = (TruePlatformerBlock1, TruePlatformerBlock1_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    # goomba that moves 4 blocks in each direction off starting block
                    enemy = Goomba9Block(column_index * tile_size, row_index * tile_size + 15)
                    AllSpriteList.add(enemy)
                if tile == 3:
                    # goomba that stays on the same block (kinda)
                    enemy = Goomba1Block(column_index * tile_size, row_index * tile_size + 15)
                    AllSpriteList.add(enemy)
                # if tile == 4:
                #     flag = Flag(column_index * tile_size, row_index * tile_size + 15)
                #     AllFlagList.add(flag) #flag is player goal, after that player will enter next level
                column_index += 1
            row_index += 1
    def draw(self):
        for tile in self.tile_list:
            # takes pic and puts it in the location of the rect cords
            background.blit(tile[0], tile[1])
            #below is code to outline blocks
            pygame.draw.rect(background, (255, 255, 255), tile[1], 2)
class Goomba9Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # load & scale image
        unsizedenemyimage = pygame.image.load('goomba.png')
        self.image = pygame.transform.scale(unsizedenemyimage, (29, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y  = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter +=1
        if abs(self.move_counter) > 220:
            self.move_direction *= -1
            self.move_counter *= -1
class Goomba1Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        unsizedenemyimage = pygame.image.load('goomba.png')
        self.image = pygame.transform.scale(unsizedenemyimage, (29, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y  = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter +=1
        if abs(self.move_counter) > 20:
            self.move_direction *= -1
            self.move_counter *= -1
world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], #full line of bricks
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #comma to seperate individual list items
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #comma to seperate individual list items
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
[1, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1], #comma to seperate individual list items
[1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
class Flag():
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        unsizedflagimage = pygame.image.load('Flag.png')
        self.image = pygame.transform.scale(unsizedflagimage, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
#creating some sprite groups
AllSpriteList = pygame.sprite.Group() #just contains enemies
AllFlagList = pygame.sprite.Group()
player = Player(100, backgroundheight - 130)# (should be) players starting pos (of lvl 1)
#AllSpriteList.add(Player)
world = World(world_data)
# load background image
backgroundPicture = pygame.image.load('Background1.png').convert()
TextFont = pygame.font.Font('freesansbold.ttf', 25)
# position arrow keys to move text
ArrowKeysToMoveX = 90
ArrowKeysToMoveY = 100
# function to display text
#prints mouse position every 2 seconds
def mousepos():
    time.sleep(2)
    mouse_pos = pygame.mouse.get_pos()
    print(mouse_pos)
#text that tells player how to move
def KeysToMoveText(x, y):
    RenderKeysToMoveText = TextFont.render("Use arrow keys to move!", True, (0, 0, 0))
    background.blit(RenderKeysToMoveText, (x, y))
run = True
#pos of buttons
ExitButtonImg = RedoButton(770, 0, ExitButtonImage)
HomeButtonImg = RedoButton(100, 100, HomeButtonImage)
redoButton = RedoButton(backgroundwidth/2 - 100, backgroundheight/2 + 10, restartButtonImage)
#def MainMenu():
#    global InMainMenu
#    while InMainMenu:

#always do this
while run:
    clock.tick(FPS)
    background.blit(backgroundPicture, (0, 0))
    world.draw()
    if main_menu == True:
        if ExitButtonImg.draw_button():
            run = False
        if HomeButtonImg.draw_button():
            run = True
    if gameOver == 0:
        AllSpriteList.update()
    AllSpriteList.draw(background)
    gameOver = player.update(gameOver)
    if gameOver == -1:
        if redoButton.draw_button():
            player.reset(100, backgroundheight - 130)
            gameOver = 0
    AllSpriteList.update()
    AllSpriteList.draw(background)
    for event in pygame.event.get():
        if pygame.event.get(pygame.QUIT):
            run = False
    clock.tick(60)
    KeysToMoveText(ArrowKeysToMoveX, ArrowKeysToMoveY)
    pygame.display.update()
pygame.quit()
