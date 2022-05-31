import pygame
from copy import deepcopy
from random import choice, randrange

WEIGHT, HEIGHT = 10, 20  # кол-во плиток
TILE = 45
GAME_RES = WEIGHT * TILE + 300, HEIGHT * TILE
FPS = 90

# стандартный шаблон
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('comicsans', 60)
myfont_score = pygame.font.SysFont('comicsans', 40)
label_tetris = myfont.render("Tetris", 1, (255, 255, 0))
label_scores = myfont_score.render("Scores", 1, (255, 255, 255))
game_sc = pygame.display.set_mode(GAME_RES)
clock = pygame.time.Clock()

# сетка
grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(WEIGHT) for y in range(HEIGHT)]


class Figure:
    FIGURE_TYPE = [
        'I', 'O', 'Z', 'S', 'L', 'J', 'T',
    ]

    FIGURE_POS = {
        'I': [(-1, 0), (-2, 0), (0, 0), (1, 0)],
        'O': [(0, -1), (-1, -1), (-1, 0), (0, 0)],
        'Z': [(-1, 0), (-1, 1), (0, 0), (0, -1)],
        'S': [(0, 0), (-1, 0), (0, 1), (-1, -1)],
        'L': [(0, 0), (0, -1), (0, 1), (-1, -1)],
        'J': [(0, 0), (0, -1), (0, 1), (1, -1)],
        'T': [(0, 0), (0, -1), (0, 1), (-1, 0)],
    }

    FIGURE_COLOR = {
        'I': (0, 93, 106),
        'O': (255, 255, 102),
        'Z': (255, 102, 102),
        'S': (153, 255, 153),
        'L': (255, 178, 102),
        'J': (102, 178, 255),
        'T': (178, 102, 255),
    }

    def __init__(self):
        self.type = choice(self.FIGURE_TYPE)
        self.color = self.FIGURE_COLOR[self.type]
        self.figure_pos = [pygame.Rect(x + WEIGHT // 2, y + 1, 1, 1) for x, y in self.FIGURE_POS[self.type]]


figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
# игровое поле
field = [[0 for i in range(WEIGHT)] for j in range(HEIGHT)]

# движение вниз
anim_count, anim_speed, anim_limit = 0, 50, 2000

lines = 0

figure = Figure()
# следующая фигура
next_figure = Figure()

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

# проверка не выхода фигуры за границы
def check_border():
    if figure.figure_pos[i].x < 0 or figure.figure_pos[i].x > WEIGHT - 1:
        return False
    elif figure.figure_pos[i].y > HEIGHT - 1 or field[figure.figure_pos[i].y][figure.figure_pos[i].x]:
        pygame.time.wait(200)  # задержка
        return False
    return True

while True:
    dx, rotate = 0, False
    game_sc.fill(pygame.Color('black'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:  # движение фигур
            if event.key == pygame.K_LEFT:
                dx = -1
            if event.key == pygame.K_RIGHT:
                dx = 1
            if event.key == pygame.K_DOWN:
                anim_limit = 100
            if event.key == pygame.K_UP:
                rotate = True


    # # условие остановки игры
    if (
            field[figure.figure_pos[0].y][figure.figure_pos[0].x]
            or field[figure.figure_pos[1].y][figure.figure_pos[1].x]
            or field[figure.figure_pos[2].y][figure.figure_pos[2].x]
            or field[figure.figure_pos[3].y][figure.figure_pos[3].x]
    ):
        exit()

    # движение по x
    figure_old = deepcopy(figure)
    for i in range(4):
        figure.figure_pos[i].x += dx
        if not check_border():
            figure = deepcopy(figure_old)
            break

    # движение по y
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure.figure_pos[i].y += 1
            if not check_border():
                for i in range(4):
                    field[figure_old.figure_pos[i].y][figure_old.figure_pos[i].x] = figure.color
                # создание новой фигуры
                figure = next_figure
                next_figure = Figure()
                anim_limit = 2000
                break

    # поворот
    center = figure.figure_pos[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure.figure_pos[i].y - center.y
            y = figure.figure_pos[i].x - center.x
            figure.figure_pos[i].x = center.x - x
            figure.figure_pos[i].y = center.y + y
            if not check_border():
                figure = deepcopy(figure_old)
                break

    # проверка
    line, lines = HEIGHT - 1, 0
    for row in range(HEIGHT - 1, -1, -1):
        count = 0
        for i in range(WEIGHT):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < WEIGHT:
            line -= 1
        else:
            anim_speed += 10
            lines += 1

    # score
    score += scores[lines]

    # построение сетки
    [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]

    # построение фигуры
    for i in range(4):
        figure_rect.x = figure.figure_pos[i].x * TILE
        figure_rect.y = figure.figure_pos[i].y * TILE
        pygame.draw.rect(game_sc, figure.color, figure_rect)

    # построение поля
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(game_sc, col, figure_rect)

    game_sc.blit(label_tetris, (485, -10))
    game_sc.blit(label_scores, (485, 100))
    game_sc.blit(myfont_score.render(str(score), True, pygame.Color('white')), (650, 100))

    # # draw next figure
    for i in range(4):
        figure_rect.x = next_figure.figure_pos[i].x * TILE + 380
        figure_rect.y = next_figure.figure_pos[i].y * TILE + 185
        pygame.draw.rect(game_sc, next_figure.color, figure_rect)

    pygame.display.flip()
    clock.tick(FPS)
