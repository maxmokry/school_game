import pygame
import datetime

from pac_man_blocks import Wall, Space, Pacman, Cookie, Block, Enemy


class Field:
    pacman_pos_x = None
    pacman_pos_y = None
    move_steps = 150
    current_step = 0
    max_x = None
    max_y = None
    enemies = []

    def __init__(self, source_map, screen: pygame.Surface, size):
        self.screen = screen
        self.size = size
        self.pacman = None

        self.blocks = {
            Wall.typ: Wall,
            Space.typ: Space,
            Pacman.typ: Pacman,
            Cookie.typ: Cookie,
            Enemy.typ: Enemy
        }
        self.map = []
        for row in source_map:
            line = []
            for cell in row:
                block_class = self.blocks.get(cell)
                if block_class:
                    block = block_class(self.screen, self.size)
                    if block.typ == 'P':
                        self.pacman = block
                    if block.typ == 'E':
                        self.enemies.append(block)
                    line.append(block)
                else:
                    raise ValueError(f'Невірний тип блоку {cell}')
            self.map.append(line)
        self.max_y = len(source_map) - 1
        self.max_x = len(source_map[0]) - 1

    def draw(self):
        y = 0
        for row in self.map:
            x = 0
            for block in row:
                # if block.typ == 'S' and (datetime.datetime.today() - block.create_time) > datetime.timedelta(seconds=5):
                #     block = Cookie(self.screen, self.size)
                block.draw(x, y)
                x += 1
            y += 1
        # score = self.score()
        # self.screen.blit(score, (0, y * self.size))

    def score(self):
        pygame.font.init()
        my_font = pygame.font.SysFont("Helvetica", 30)
        text = my_font.render(f"Score: {self.pacman.score}", True, "White")
        surface = pygame.Surface((self.size * len(self.map[0]), self.size))
        surface.blit(text, (0, 0))
        return surface

    def pacman_move(self, direction):
        destination_x = self.pacman.x
        destination_y = self.pacman.y
        if direction == 'left':
            destination_x = self.pacman.x - 1
            if destination_x < 0:
                destination_x = self.max_x
        if direction == 'right':
            destination_x = self.pacman.x + 1
            if destination_x > self.max_x:
                destination_x = 0
        if direction == 'up':
            destination_y = self.pacman.y - 1
            if destination_y < 0:
                destination_y = self.max_y
        if direction == 'down':
            destination_y = self.pacman.y + 1
            if destination_y > self.max_y:
                destination_y = 0

        destination_block: Block = self.map[destination_y][destination_x]
        if destination_block.typ in [' ', 'S', 'E']:
            # if destination_block.typ == ' ':
            #     self.pacman.score += 1
            self.map[self.pacman.y][self.pacman.x] = self.blocks['S'](self.screen, self.size)
            self.map[destination_y][destination_x] = self.pacman
            self.pacman.current_step = 1

    def pacman_is_moving(self):
        if self.pacman.current_step == 0:
            return False
        else:
            self.pacman.current_step += 1
            if self.pacman.current_step >= self.move_steps:
                self.pacman.current_step = 0
            return True

    def intersect(self):
        for enemy in self.enemies:
            if enemy.x == self.pacman.x and enemy.y == self.pacman.y:
                self.pacman.dead()
                return False
        return True

    def enemy_move(self, enemy: Enemy):
        if not enemy.direction:
            enemy.random_direction()
        direction = enemy.direction
        destination_x = enemy.x
        destination_y = enemy.y
        if direction == 'left':
            destination_x = enemy.x - 1
            if destination_x < 0:
                destination_x = self.max_x
        if direction == 'right':
            destination_x = enemy.x + 1
            if destination_x > self.max_x:
                destination_x = 0
        if direction == 'up':
            destination_y = enemy.y - 1
            if destination_y < 0:
                destination_y = self.max_y
        if direction == 'down':
            destination_y = enemy.y + 1
            if destination_y > self.max_y:
                destination_y = 0

        destination_block: Block = self.map[destination_y][destination_x]
        if destination_block.typ in [' ', 'S', 'P']:
            self.map[enemy.y][enemy.x] = self.blocks[enemy.prev_block](self.screen, self.size)
            enemy.prev_block = destination_block.typ
            self.map[destination_y][destination_x] = enemy
            enemy.current_step = 1
        else:
            enemy.random_direction()

    def enemies_move(self):
        for enemy in self.enemies:
            if not enemy.is_moving(self.move_steps):
                self.enemy_move(enemy)

