import pygame
from os import listdir
from os.path import isfile, join
from random import choice, randint


pygame.init()

ROW = COL = 15
SQ_SIZE = 80
WIDTH, HEIGHT = COL * SQ_SIZE, ROW * SQ_SIZE
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wave Function Collapse")

BLACK = (0, 0, 0)
WHITE = (220, 220, 220)

# ['blank.png', 'down.png', 'left.png', 'right.png', 'up.png']
BLANK = 0
DOWN = 1
LEFT = 2
RIGHT = 3
UP = 4

PATH = "tiles\\roads"
FILE_NAMES = [f for f in listdir(PATH) if isfile(join(PATH, f))]
TILES = [
    pygame.transform.scale(
        pygame.image.load(join(PATH, name)), (SQ_SIZE - 2, SQ_SIZE - 2)
    )
    for name in FILE_NAMES
]

# DEPENDS ON THE TILE IMAGES
rules = {
    BLANK: [
        [BLANK, UP],  # to the up
        [BLANK, RIGHT],  # to the right
        [BLANK, DOWN],  # to the down
        [BLANK, LEFT],  # to the left
    ],
    UP: [
        [RIGHT, LEFT, DOWN],
        [LEFT, UP, DOWN],
        [BLANK, DOWN],
        [DOWN, RIGHT, UP],
    ],
    RIGHT: [
        [RIGHT, LEFT, DOWN],
        [LEFT, UP, DOWN],
        [RIGHT, LEFT, UP],
        [BLANK, LEFT],
    ],
    DOWN: [
        [BLANK, UP],
        [LEFT, UP, DOWN],
        [RIGHT, LEFT, UP],
        [RIGHT, UP, DOWN],
    ],
    LEFT: [
        [RIGHT, LEFT, DOWN],
        [BLANK, RIGHT],
        [RIGHT, LEFT, UP],
        [UP, DOWN, RIGHT],
    ],
}


class Cell:
    def __init__(self):
        self.collapsed = False
        self.options = [BLANK, DOWN, LEFT, RIGHT, UP]

    def __repr__(self):
        return str(len(self.options))


def main():
    clock = pygame.time.Clock()
    running = True
    grid = [[Cell() for _ in range(ROW)] for _ in range(COL)]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        grid = update(grid)
        pygame.display.update()
        clock.tick(15)
    pygame.quit()
    quit()


def check_valid(arr, valid):
    output = []
    for i in range(len(arr)):
        if arr[i] in valid:
            output.append(arr[i])
    return output


# todo: once it comes to end program stops
def update(grid):
    WIN.fill(BLACK)
    for i in range(ROW):
        for j in range(COL):
            cell = grid[i][j]
            if cell.collapsed:  # collapsed => only one option
                index = cell.options[0]
                image = TILES[index]
                WIN.blit(image, (j * SQ_SIZE, i * SQ_SIZE))

    grid_copy = [item for sublist in grid for item in sublist]
    grid_copy = list(filter(lambda x: not x.collapsed, grid_copy))
    grid_copy.sort(key=lambda x: len(x.options), reverse=False)
    stop_index = 0
    length = len(grid_copy[0].options)
    for i in range(len(grid_copy)):
        if len(grid_copy[i].options) > length:
            stop_index = i
            break
    if stop_index > 0:
        grid_copy = grid_copy[0:stop_index]
    cell = choice(grid_copy)
    cell.collapsed = True
    pick = choice(cell.options)
    cell.options = [pick]

    next_grid = [[0 for _ in range(ROW)] for _ in range(COL)]
    for i in range(ROW):
        for j in range(COL):
            next_grid[i][j] = grid[i][j]
            if not grid[i][j].collapsed:
                options = [BLANK, DOWN, LEFT, RIGHT, UP]
                # Look up
                if i > 0:
                    up = grid[i - 1][j]
                    valid_options = []
                    for option in up.options:
                        valid = rules[option][2]
                        for element in valid:
                            if element not in valid_options:
                                valid_options.append(element)
                    options = check_valid(options, valid_options)
                # Look right
                if j < COL - 1:
                    right = grid[i][j + 1]
                    valid_options = []
                    for option in right.options:
                        valid = rules[option][3]
                        for element in valid:
                            if element not in valid_options:
                                valid_options.append(element)
                    options = check_valid(options, valid_options)
                # Look down
                if i < ROW - 1:
                    down = grid[i + 1][j]
                    valid_options = []
                    for option in down.options:
                        valid = rules[option][0]
                        for element in valid:
                            if element not in valid_options:
                                valid_options.append(element)
                    options = check_valid(options, valid_options)
                # Look left
                if j > 0:
                    left = grid[i][j - 1]
                    valid_options = []
                    for option in left.options:
                        valid = rules[option][1]
                        for element in valid:
                            if element not in valid_options:
                                valid_options.append(element)
                    options = check_valid(options, valid_options)
                next_grid[i][j].options = options

    return next_grid


if __name__ == "__main__":
    main()
