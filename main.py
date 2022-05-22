import pygame
import random
import math
from pygame import mixer
import cv2


# initialize the pygame
pygame.init()

# create screen of resolution 800*600
screen = pygame.display.set_mode((800, 600))

bg = pygame.image.load('Images/bg.jpg')


#title and icon
pygame.display.set_caption("3093 - A Dark Future")
icon = pygame.image.load('Images/soldier.png')
pygame.display.set_icon(icon)


# player
playerImg = pygame.image.load('Images/aircraft.png')
playerx = 370
playery = 480
playerx_change = 0

enemy1 = []
enemy1x = []
enemy1y = []
enemy1x_change = []
enemy1y_change = []
num_of_enemies = 3

for i in range(num_of_enemies):
    enemy1.append(pygame.image.load('Images/ufo1.png'))
    enemy1x.append(random.randint(0, 735))
    enemy1y.append(random.randint(50, 150))
    enemy1x_change.append(0.6)
    enemy1y_change.append(40)

bullet = pygame.image.load('Images/missile.png')
bulletx = 0
bullety = 480
bulletx_change = 0
bullety_change = 2.0
bullet_state = "ready"
# ready - can't see on screen
# fire - can see on screene

score_value = 0
font = pygame.font.Font('Fonts/Nebula-Regular.ttf', 20)

bulused = 1
avgsc = 0
logo = pygame.image.load('Images/7FPS_.png')


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def show_start_screen():
    # screen.fill((255,255,255))
    screen.blit(logo, (255, 255))


def show_bull(x, y):
    bull = font.render("Bullets Used: " + str(bulused-1),
                       True, (255, 255, 255))
    screen.blit(bull, (x, y))


def show_avg(x, y):
    avg = font.render("Average Hit: " + str(avgsc), True, (255, 255, 255))
    screen.blit(avg, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemy1[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x+16, y+10))


def isCollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt(
        (math.pow(enemyx-bulletx, 2) + math.pow(enemyy-bullety, 2)))
    if distance < 27:
        return True
    else:
        return False


overfont = pygame.font.Font('Fonts/Nebula-Regular.ttf', 45)


def game_over_text():
    over_text = overfont.render(
        "YOUR SPACESHIP IS DEAD", True, (255, 255, 255))
    screen.blit(over_text, (10, 220))


# t_end = time.time() + 5
# while time.time() < t_end:
#     show_start_screen()
# game loop
running = True
death = True
onclick = True


def play():
    global running, death, onclick, playerx, playerImg, playerx, playery, playerx_change, enemy1, enemy1x, enemy1y, enemy1x_change, enemy1y_change, num_of_enemies, bullet, bulletx, bullety, bulletx_change, bullety_change, bullet_state, score_value, font, bulused, avgsc, logo, event, vidintro

    bruh_sound = mixer.Sound('Audios/bruh.mp3')
    bruh_sound.play()
    # bg sound
    mixer.music.load('Audios/space.mp3')
    mixer.music.play(-1)

    while running:

        screen.fill((51, 51, 51))
        screen.blit(bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # print("A key has been pressed")
                if event.key == pygame.K_LEFT:
                    playerx_change = -0.6

                if event.key == pygame.K_RIGHT:
                    playerx_change = 0.6

                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bull_sound = mixer.Sound('Audios/missile.mp3')
                        bull_sound.play()
                        bulused += 1
                        bulletx = playerx
                        fire_bullet(bulletx, bullety)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerx_change = 0

        playerx += playerx_change

        if playerx <= 0:
            playerx = 0
        elif playerx >= 736:
            playerx = 736

        for i in range(num_of_enemies):

            # game over
            if enemy1y[i] > 200:
                for j in range(num_of_enemies):
                    enemy1y[j] = 2000
                    playerx = 2000
                    bulletx = 2000
                    bullet_state = "fire"
                if death:
                    game_over_text()
                    bruh_sound = mixer.Sound('Audios/bruh.mp3')
                    bruh_sound.play()
                    death = False
                dead_text = font.render("YOU DIED", True, (255, 255, 255))
                over_text = font.render(
                    "LOL REOPEN THE GAME TO RESTART THE GAME", True, (255, 255, 255))
                screen.blit(over_text, (70, 270))
                screen.blit(dead_text, (350, 200))

                if event.type == pygame.KEYDOWN:
                    # print("A key has been pressed")
                    if event.key == pygame.K_RETURN:
                        # running = False
                        if onclick:
                            print('bruh')
                            onclick = False
                            bulletx = 0
                            bullety = 480
                            bulletx_change = 0
                            bullety_change = 2.0
                            bullet_state = "ready"
                            playerx = 370
                            playerx = 370
                            playery = 480
                            playerx_change = 0

                            enemy1 = []
                            enemy1x = []
                            enemy1y = []
                            enemy1x_change = []
                            enemy1y_change = []
                            num_of_enemies = 3
                            running = True
                            death = True
                            onclick = True
                            play()
                break

            enemy1x[i] += enemy1x_change[i]

            if enemy1x[i] <= 0:
                enemy1x_change[i] = 0.5
                enemy1y[i] += enemy1y_change[i]
            elif enemy1x[i] >= 736:
                enemy1x_change[i] = -0.5
                enemy1y[i] += enemy1y_change[i]

            # collision
            collision = isCollision(enemy1x[i], enemy1y[i], bulletx, bullety)
            if collision:
                expl_sound = mixer.Sound('Audios/explosion.mp3')
                expl_sound.play()
                bullety = 480
                bullet_state = "ready"
                score_value += 1
                # print(score_value)
                enemy1x[i] = random.randint(0, 735)
                enemy1y[i] = random.randint(50, 150)

            enemy(enemy1x[i], enemy1y[i], i)

        # bullet movement

        if bullety <= 0:
            bullety = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletx, bullety)
            bullety -= bullety_change

        avgsc = (1.0 + score_value - 1) / (1.0 + bulused - 1)

        player(playerx, playery)
        enemy(enemy1x[i], enemy1y[i], i)
        show_score(0, 500)
        show_bull(0, 550)
        show_avg(500, 550)
        pygame.display.update()


def intro():
    video = cv2.VideoCapture("Videos/inner-rau.mp4")
    success, video_image = video.read()
    fps = video.get(cv2.CAP_PROP_FPS)

    window = pygame.display.set_mode(video_image.shape[1::-1])
    clock = pygame.time.Clock()

    run = success
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        success, video_image = video.read()
        if success:
            video_surf = pygame.image.frombuffer(
                video_image.tobytes(), video_image.shape[1::-1], "BGR")
        else:
            run = False
        window.blit(video_surf, (0, 0))
        pygame.display.flip()

intro()
play()
