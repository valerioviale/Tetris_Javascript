import pygame, random

pygame.init()

WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
WHITE = (200, 200, 200)
GREY = (128, 128, 128)
BLACK = (10, 10, 10)
FUCHSIA = (255, 0, 255)

tetrominoes = [
    [[1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]]
]

tetromino_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (128, 0, 128)]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
current_tetromino = None
current_tetromino_color = None
x, y = 0, 0

score = 0
score_to_change_color = 5

font = pygame.font.Font(None, 36)

shadow_color = GREY

def rotate_tetromino():
    global current_tetromino
    current_tetromino = [list(row) for row in zip(*current_tetromino[::-1])]

def draw_grid():
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if grid[row][col]:
                pygame.draw.rect(screen, tetromino_colors[grid[row][col] - 1],
                                 pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
    for row in range(len(current_tetromino)):
        for col in range(len(current_tetromino[row])):
            if current_tetromino[row][col]:
                pygame.draw.rect(screen, current_tetromino_color,
                                 pygame.Rect((x + col) * GRID_SIZE, (y + row) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
                pygame.draw.rect(screen, shadow_color,
                                 pygame.Rect((x + col) * GRID_SIZE, (y + row) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 2)

def new_tetromino():
    global current_tetromino, current_tetromino_color, x, y
    current_tetromino = random.choice(tetrominoes)
    current_tetromino_color = random.choice(tetromino_colors)
    x = GRID_WIDTH // 2 - len(current_tetromino[0]) // 2
    y = 0

def collide():
    for row in range(len(current_tetromino)):
        for col in range(len(current_tetromino[row])):
            if current_tetromino[row][col]:
                if x + col < 0 or x + col >= GRID_WIDTH or y + row >= GRID_HEIGHT or grid[y + row][x + col]:
                    return True
    return False

def place_tetromino():
    for row in range(len(current_tetromino)):
        for col in range(len(current_tetromino[row])):
            if current_tetromino[row][col]:
                grid[y + row][x + col] = tetromino_colors.index(current_tetromino_color) + 1
    check_lines()

def check_lines():
    global score
    full_lines = []
    for row in range(GRID_HEIGHT):
        if all(grid[row]):
            full_lines.append(row)
    for row in full_lines:
        del grid[row]
        grid.insert(0, [0] * GRID_WIDTH)
        score += 10

clock = pygame.time.Clock()
new_tetromino()
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= 1
                if collide():
                    x += 1
            if event.key == pygame.K_RIGHT:
                x += 1
                if collide():
                    x -= 1
            if event.key == pygame.K_DOWN:
                y += 1
                if collide():
                    y -= 1
            if event.key == pygame.K_UP:
                rotate_tetromino()
                if collide():
                    rotate_tetromino()

    y += 1
    if collide():
        y -= 1
        place_tetromino()
        score += 1
        new_tetromino()
        if collide():
            game_over = True

    screen.fill(BLACK)
    draw_grid()

    text = font.render("Points: " + str(score), True, FUCHSIA)
    screen.blit(text, (10, 10))

    pygame.display.update()
    clock.tick(5)
pygame.quit()
