import pygame


class Block:
    typ = None

    def __init__(self, screen, size):
        self.screen = screen
        self.size = size
        self.surface = pygame.Surface((size, size))
        self.shape()

    def shape(self):
        pygame.draw.rect(self.surface, "White", (0, 0, self.size, self.size))

    def draw(self, x, y):
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

    def shape(self):
        center = int(self.size / 2)
        radius = int(self.size / 3)
        pygame.draw.circle(self.surface, 'Orange', (center, center), radius=radius)
