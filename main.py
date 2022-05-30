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

# координаты плиток фигур
figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figures = [[pygame.Rect(x + WEIGHT // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
# игровое поле
field = [[0 for i in range(WEIGHT)] for j in range(HEIGHT)]

# движение вниз
anim_count, anim_speed, anim_limit = 0, 50, 2000

lines = 0

figure = deepcopy(choice(figures))

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}


# проверка не выхода фигуры за границы
def check_border():
    if figure[i].x < 0 or figure[i].x > WEIGHT - 1:
        return False
    elif figure[i].y > HEIGHT - 1 or field[figure[i].y][figure[i].x]:
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

    # условие остановки игры
    if (
            field[figure[0].y][figure[0].x]
            or field[figure[1].y][figure[1].x]
            or field[figure[2].y][figure[2].x]
            or field[figure[3].y][figure[3].x]
    ):
        exit()

    # движение по x
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_border():
            figure = deepcopy(figure_old)
            break

    # движение по y
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_border():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = pygame.Color('white')
                # создание новой фигуры
                figure = deepcopy(choice(figures))
                anim_limit = 2000
                break

    # поворот
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_border():
                figure = deepcopy(figure_old)
                break

    # check lines
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
            anim_speed += 3
            lines += 1

    # score
    score += scores[lines]

    # построение сетки
    [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]

    # построение фигуры
    for i in range(4):
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(game_sc, pygame.Color('white'), figure_rect)

    # построение поля
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(game_sc, col, figure_rect)

    game_sc.blit(label_tetris, (485, -10))
    game_sc.blit(label_scores, (485, 100))
    game_sc.blit(myfont_score.render(str(score), True, pygame.Color('white')), (650, 100))

    pygame.display.flip()
    clock.tick(FPS)
