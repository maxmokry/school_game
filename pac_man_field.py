from pac_man_blocks import Wall, Space, Pacman, Cookie, Block, Enemy


class Field:
    pacman_pos_x = None
    pacman_pos_y = None
    move_steps = 50
    current_step = 0
    max_x = None
    max_y = None
    enemies = []

    def __init__(self, source_map, screen, size):
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
                block.draw(x, y)
                x += 1
            y += 1

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
        if destination_block.typ in [' ', 'S']:
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
