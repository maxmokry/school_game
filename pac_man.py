import pygame
import sys
from pac_man_field import Field
from pac_man_map import source_map


# Pygame initialization
pygame.init()

# set window size
block_size = 40
width = block_size * len(source_map[0])
height = block_size * len(source_map)
screen = pygame.display.set_mode((width, height))
running = True

field = Field(source_map, screen, block_size)

while running:

    keys = pygame.key.get_pressed()

    if not field.pacman_is_moving():
        if keys[pygame.K_LEFT]:
            field.pacman_move('left')
        elif keys[pygame.K_RIGHT]:
            field.pacman_move('right')
        elif keys[pygame.K_UP]:
            field.pacman_move('up')
        elif keys[pygame.K_DOWN]:
            field.pacman_move('down')

    field.draw()
    pygame.display.update()
    running = field.intersect()

    # Game quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()
