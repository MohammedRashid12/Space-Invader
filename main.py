import pygame
import random
import math
#initialize the pygame
pygame.init()
#create display screen size 800pixels by 600pixels
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('7871.jpg')


#player
playerImg = pygame.image.load('player.png')
playerx = 370
playery = 480
playerx_change=0

#enemy
enemyImg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('planet.png'))
    enemyx.append(random.randint(0, 736))
    enemyy.append(random.randint(50, 150))
    enemyx_change.append(0.1)
    enemyy_change.append(40)


#bullet

#Ready - You can't see the bullet on the screen
#Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletx = 0
bullety = 480
bulletx_change=0
bullety_change=0.3
bullet_state="ready"

# Displaying score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textx = 10
texty = 10

# game over text
over_font = pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    score = font.render("Score : " + str(score_value), True, (225,255,255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (225, 255, 255))
    screen.blit(over_text, (200, 250))
def player(x,y):
    screen.blit(playerImg, (x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((math.pow(enemyx-bulletx, 2)) + (math.pow(enemyy-bullety, 2)))
    if distance<27:
        return True
    else:
        return False

#Game loop that makes the loop doesn't close down
running = True
while running:

    # changing screen background color
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0,0))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -0.125
            if event.key == pygame.K_RIGHT:
                playerx_change = 0.125
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletx = playerx
                    fire_bullet(bulletx,bullety)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    #calling player to render into the screen
    playerx +=playerx_change #rendering player mechanics to move to right or left

    #creating boundaries
    if playerx <=0:
       playerx =0
    elif playerx >=736:
        playerx= 736



    # creating boundaries
    for i in range(num_of_enemies):
        # game over
        if enemyy[i] > 440:
            for j in range(num_of_enemies):
                enemyy[j] = 2000
            game_over_text()
            break
        enemyx[i] +=enemyx_change[i]
        if enemyx[i] <= 0:
            enemyx_change[i] = 0.1
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 736:
            enemyx_change[i] = -0.1
            enemyy[i] += enemyy_change[i]

    # Checking for collisions
        collision = isCollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            bullety = 480
            bullet_state = "ready"
            score_value += 1
            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(50, 150)

        enemy(enemyx[i], enemyy[i],i)

    #bullet movement
    if bullety <=0:
        bullety=480
        bullet_state="ready"

    if bullet_state is "fire":
        fire_bullet(bulletx,bullety)
        bullety -= bullety_change



    player(playerx,playery)
    show_score(textx,texty)
    pygame.display.update()