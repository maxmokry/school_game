import pygame
import sys

# Pygame initialization
pygame.init()

# set window size
width, height = 1280, 640
screen = pygame.display.set_mode((width, height))
background = pygame.image.load('images/backgrounds/bg1.png')

# main cycle
running = True
bg_position = 0
while running:

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        bg_position -= 1
    elif keys[pygame.K_RIGHT]:
        bg_position += 1
    elif keys[pygame.K_r]:
        bg_position = 0

    if abs(bg_position) >= width:
        bg_position = 0

    # screen clearing
    screen.blit(background, (0 + bg_position, 0))
    screen.blit(background, (width + bg_position, 0))
    screen.blit(background, (-width + bg_position, 0))


    # screen update
    pygame.display.update()

    # Game quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Завершение программы
pygame.quit()
sys.exit()
