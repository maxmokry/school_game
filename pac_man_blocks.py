import pygame
import random
import datetime


class Block:
    typ = None
    current_step = 0

    def __init__(self, screen, size):
        self.screen = screen
        self.size = size
        self.surface = pygame.Surface((size, size))
        self.shape()
        self.create_time = datetime.datetime.now()

    def shape(self):
        pygame.draw.rect(self.surface, "White", (0, 0, self.size, self.size))

    def draw(self, x, y):
        self.x = x
        self.y = y
        pos_x = self.size * x
        pos_y = self.size * y
        self.screen.blit(self.surface, (pos_x, pos_y))


class Wall(Block):
    typ = "X"

    def shape(self):
        pygame.draw.rect(self.surface, "Blue", (0, 0, self.size, self.size), border_radius=5)


class Cookie(Block):
    typ = ' '

    def shape(self):
        center = int(self.size / 2)
        radius = int(self.size / 8)
        pygame.draw.circle(self.surface, 'Yellow', (center, center), radius=radius)


class Space(Block):
    typ = 'S'

    def shape(self):
        pass


class Pacman(Block):
    typ = 'P'
    score = 0

    def shape(self, size=None):
        if size is None:
            size = self.size
        center = int(size / 2)
        radius = int(size / 3)
        pygame.draw.circle(self.surface, 'Orange', (center, center), radius=radius)

    def dead(self):
        size = self.size
        for i in range(10):
            size += 10
            self.surface = pygame.Surface((size, size))
            self.shape(size)
            x = self.x
            y = self.y
            self.draw(x, y)
            pygame.display.update()


class Enemy(Block):
    typ = "E"
    colors = ['Green', 'Red', 'Yellow']
    prev_block = ' '
    direction = None

    def shape(self):
        color = random.choice(self.colors)
        size = int(self.size / 2)
        x = 0 + int(size / 2)
        y = 0 + int(size / 2)
        pygame.draw.rect(self.surface, color, (x, y, size, size), border_radius=3)

    def random_direction(self):
        self.direction = random.choice(['left', 'right', 'up', 'down'])

    def is_moving(self, max_steps):
        if self.current_step == 0:
            return False
        else:
            self.current_step += 1
            if self.current_step >= max_steps:
                self.current_step = 0
                return False
            return True

