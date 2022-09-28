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
#global gameOver
gameOver = 0
# are we in the main menu
InMainMenu = True
#define colors
White = [255, 255, 255]
Black = [0, 0, 0]
Red = [255, 0, 0]
Orange = [232, 74, 35]
Yellow = [219, 232, 35]
LightGreen = [19, 230, 111]
Blue = [29, 104, 189]
Purple = [136, 29, 189]
#load images
restartButtonImage = pygame.image.load('Redo Button.png')
ExitButtonImage = pygame.image.load('Exit.png')
HomeButtonImage = pygame.image.load('Home button.png')
# circle sizes
circle1size = [94, 94]
circle2size = [50, 50]
circle3size = [69, 69]
circle4size = [90, 90]
circle5size = [70, 70]
CircleSizeList = [circle1size, circle2size, circle3size, circle4size, circle5size]
#load circles for level (must be loaded seperately so we can change colors when needed)
level1circleUnscaled = pygame.image.load('1circle.png')
level1circle = pygame.transform.scale(level1circleUnscaled, circle1size)
level2circleUnscaled = pygame.image.load('2circle.png')
level2circle = pygame.transform.scale(level2circleUnscaled, circle2size)
level3circleUnscaled = pygame.image.load('3circle.png')
level3circle = pygame.transform.scale(level3circleUnscaled, circle3size)
level4circleUnscaled = pygame.image.load('4circle.png')
level4circle = pygame.transform.scale(level4circleUnscaled, circle4size)
level5circleUnscaled = pygame.image.load('5circle.png')
level5circle = pygame.transform.scale(level5circleUnscaled, circle5size)
#load the main menu map without circles
MainMenuMap = pygame.image.load('empty map.png')
#list of all level circles
LevelCircles = [level1circle, level2circle, level3circle, level4circle, level5circle]
#where the circles will appear when called
Level_Label_Pos =  [[60,95], [269,210], [390,100], [570,90], [670,255]]
#what level are we in
CurrentLevel = 2
CurrentLevelMinusOne = CurrentLevel - 1
#classes
class Button():
    def __init__(self, x, y, height, width, image):
        self.image = image
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
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
                print(str(self) + " is clicked")
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
            if CurrentLevel == 1:
                for tile in Level1World.tile_list:
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
            if CurrentLevel == 2:
                for tile in Level2World.tile_list:
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
                AllFlagList.empty()

            self.rect.x += dx
            self.rect.y += dy

        elif gameOver == -1:
            self.image = self.deadImage
            if self.rect.y > -100:
                self.rect.y -= 3
        elif gameOver == 1:
            level_finished()
            print ("level finished")
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
        self.deadImage = pygame.transform.scale(deadImg, (50, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.SpriteWidth = self.image.get_width()
        self.SpriteHeight = self.image.get_height()
        self.Speed = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True
# player creation
player = Player(0, 0)
CircleHitBoxList = []
def level_finished():
    global CurrentLevel
    global InMainMenu
    global CurrentLevelMinusOne
    global gameOver
    gameOver = 0
    player.reset(0, 0)
    CurrentLevelMinusOne = CurrentLevelMinusOne + 1
    InMainMenu = True
    print(CurrentLevel)
for i in range(len(LevelCircles)):
    circleRect = [Level_Label_Pos[i][0], Level_Label_Pos[i][1], CircleSizeList[i][0], CircleSizeList[i][1]]
    CircleHitBoxList.append(circleRect)

def DrawMap():
    #CircleHitBoxList = []
    for i in range(len(LevelCircles)):
        background.blit(MainMenuMap,[100,100])
        circleRect = [Level_Label_Pos[i][0], Level_Label_Pos[i][1], CircleSizeList[i][0], CircleSizeList[i][1]]
        #CircleHitBoxList.append(circleRect)

        if i < CurrentLevelMinusOne:
            CircleColor = LightGreen
        elif i == CurrentLevelMinusOne:
            CircleColor = Yellow
        else:
            CircleColor = Red
        pygame.draw.ellipse(background, CircleColor, circleRect)
        background.blit(LevelCircles[i], Level_Label_Pos[i])
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
                if tile == 4:
                    flag = Flag(column_index * tile_size, row_index * tile_size + 15)
                    AllFlagList.add(flag) #flag is player goal, after that player will enter home screen
                    AllSpriteList.add(flag)
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
world_data_1 = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], #full line of bricks
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #comma to seperate individual list items
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #comma to seperate individual list items
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1], #comma to seperate individual list items
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
world_data_2 = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], #full line of bricks
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #comma to seperate individual list items
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #comma to seperate individual list items
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1], #comma to seperate individual list items
[1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
world_data_3 = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
world_data_4 = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
world_data_5 = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1], #comma to seperate individual list items
[1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

class Flag(pygame.sprite.Sprite):
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
#AllSpriteList.add(Player)
Level1World = World(world_data_1)
Level2World = World(world_data_2)
#Level3World = World(world_data_3)
#Level4World = World(world_data_4)
#Level5World = World(world_data_5)
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
ExitButtonImg = Button(900, 0, 50, 100, ExitButtonImage,)
HomeButtonImg = Button(0, 0, 50, 50, HomeButtonImage)
redoButton = Button(450, 0, 50, 100, restartButtonImage)
ShowLockedLevelMessage = False
ShowMessageStartTime = 0
MainMenuTimer = 0
RenderCantGoToNextLevelText = TextFont.render("Level locked! Complete the level in yellow to unlock the next level.", True, (0, 0, 0))
def LevelClicked(CurrentLevel):
    global InMainMenu
    InMainMenu = False
    if CurrentLevel == 1:
        print("level 1 clicked")
        player.rect.x = 100
        player.rect.y = 300
    if CurrentLevel == 2:
        print("level 2 clicked")
        player.rect.x = 200
        player.rect.y = 300
def MainMenu():
    global InMainMenu, run, CurrentLevel, ShowLockedLevelMessage, MainMenuTimer, ShowMessageStartTime, RenderCantGoToNextLevelText
    while InMainMenu:
        for event in pygame.event.get():
            if event.type == (pygame.QUIT):
                run = False
                InMainMenu= False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(CircleHitBoxList)):
                    if pygame.Rect(CircleHitBoxList[i]).collidepoint(event.pos):
                        print("Level clicked")


                        if i <= CurrentLevelMinusOne:
                            # go to selected level
                            CurrentLevel = i + 1
                            LevelClicked(CurrentLevel)
                            InMainMenu = False

                        elif i > CurrentLevelMinusOne:
                            ShowLockedLevelMessage = True
                            ShowMessageStartTime = time.time()


        MainMenuTimer = time.time()
        background.fill((255, 255, 255))
        if ShowLockedLevelMessage and MainMenuTimer - ShowMessageStartTime < 5:
            background.blit(RenderCantGoToNextLevelText, [100, 400])
        else:
            ShowLockedLevelMessage = False
        DrawMap()
        pygame.display.flip()

print(CircleHitBoxList)
#always do this
while run:
    clock.tick(FPS)
    background.blit(backgroundPicture, (0, 0))

    if CurrentLevel == 1:
        Level1World.draw()
    if CurrentLevel == 2:
        Level2World.draw()
    if CurrentLevel == 3:
        Level2World.draw()
    if CurrentLevel == 4:
        Level2World.draw()
    if CurrentLevel == 5:
        Level2World.draw()
    if InMainMenu == True:
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
            player.reset(100, 300)
            gameOver = 0
    AllSpriteList.update()
    AllSpriteList.draw(background)
    for event in pygame.event.get():
        if event.type == (pygame.QUIT):
            run = False
            InMainMenu = False
    if HomeButtonImg.click == True:
        InMainMenu = True
    if InMainMenu:
        MainMenu()
    clock.tick(60)
    KeysToMoveText(ArrowKeysToMoveX, ArrowKeysToMoveY)
    pygame.display.update()
pygame.quit()
