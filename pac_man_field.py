from pac_man_blocks import Wall, Space, Pacman, Cookie, Block


class Field:
    pacman_pos_x = None
    pacman_pos_y = None
    move_steps = 50
    current_step = 0
    max_x = None
    max_y = None

    def __init__(self, source_map, screen, size):
        wall = Wall(screen, size)
        space = Space(screen, size)
        pacman = Pacman(screen, size)
        cookie = Cookie(screen, size)

        self.blocks = {
            wall.typ: wall,
            space.typ: space,
            pacman.typ: pacman,
            cookie.typ: cookie
        }
        self.map = []
        for row in source_map:
            line = []
            for cell in row:
                line.append(cell)
            self.map.append(line)
        self.max_y = len(source_map) - 1
        self.max_x = len(source_map[0]) - 1

    def draw(self):
        y = 0
        for row in self.map:
            x = 0
            for typ in row:
                block: Block = self.blocks.get(typ)
                if block:
                    block.draw(x, y)
                    if block.typ == 'P':
                        self.pacman_pos_x = x
                        self.pacman_pos_y = y
                x += 1
            y += 1

    def pacman_move(self, direction):
        destination_x = self.pacman_pos_x
        destination_y = self.pacman_pos_y
        if direction == 'left':
            destination_x = self.pacman_pos_x - 1
            if destination_x < 0:
                destination_x = self.max_x
        if direction == 'right':
            destination_x = self.pacman_pos_x + 1
            if destination_x > self.max_x:
                destination_x = 0
        if direction == 'up':
            destination_y = self.pacman_pos_y - 1
            if destination_y < 0:
                destination_y = self.max_y
        if direction == 'down':
            destination_y = self.pacman_pos_y + 1
            if destination_y > self.max_y:
                destination_y = 0

        destination_block = self.map[destination_y][destination_x]
        if destination_block in [' ', 'S']:
            self.map[self.pacman_pos_y][self.pacman_pos_x] = 'S'
            self.map[destination_y][destination_x] = 'P'
            self.current_step = 1

    def pacman_is_moving(self):
        if self.current_step == 0:
            return False
        else:
            self.current_step += 1
            if self.current_step >= self.move_steps:
                self.current_step = 0
            return True
