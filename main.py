# Snake Game in Python (Pygame)
# Run this in VS Code. First install pygame: pip install pygame

import pygame
import random
import sys
from pathlib import Path

# ---------- Settings ----------
CELL_SIZE = 25
GRID_CELLS = 24  # 24x24 grid
WIDTH = HEIGHT = CELL_SIZE * GRID_CELLS
FPS_START = 10          # starting speed
FPS_INCREMENT_EVERY = 5 # increase speed every N points
FONT_NAME = "consolas"

# Colors (R, G, B)
BG = (20, 20, 24)
GRID = (33, 36, 44)
SNAKE_HEAD = (0, 200, 120)
SNAKE_BODY = (0, 160, 96)
FOOD = (220, 80, 90)
TEXT = (230, 230, 235)
SHADOW = (0, 0, 0)

# High score file
HS_FILE = Path.home() / ".snake_highscore.txt"

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def grid_to_px(cell):
    x, y = cell
    return x * CELL_SIZE, y * CELL_SIZE


def random_empty_cell(snake):
    while True:
        cell = (random.randrange(GRID_CELLS), random.randrange(GRID_CELLS))
        if cell not in snake:
            return cell


def draw_grid(surface):
    for x in range(GRID_CELLS):
        pygame.draw.line(surface, GRID, (x * CELL_SIZE, 0), (x * CELL_SIZE, HEIGHT))
    for y in range(GRID_CELLS):
        pygame.draw.line(surface, GRID, (0, y * CELL_SIZE), (WIDTH, y * CELL_SIZE))


def draw_rect(surface, color, cell, radius=6):
    x, y = grid_to_px(cell)
    rect = pygame.Rect(x+1, y+1, CELL_SIZE-2, CELL_SIZE-2)
    pygame.draw.rect(surface, color, rect, border_radius=radius)


def load_high_score():
    try:
        if HS_FILE.exists():
            return int(HS_FILE.read_text().strip())
    except Exception:
        pass
    return 0


def save_high_score(score):
    try:
        HS_FILE.write_text(str(score))
    except Exception:
        pass


def render_text(surface, text, size, pos, color=TEXT, center=False, shadow=True):
    font = pygame.font.SysFont(FONT_NAME, size, bold=True)
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = pos
    else:
        rect.topleft = pos
    if shadow:
        shadow_surf = font.render(text, True, SHADOW)
        shadow_rect = shadow_surf.get_rect(center=rect.center)
        shadow_rect.move_ip(2, 2)
        surface.blit(shadow_surf, shadow_rect)
    surface.blit(surf, rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake - Python/Pygame")
    clock = pygame.time.Clock()

    high_score = load_high_score()

    def reset_game():
        start = (GRID_CELLS // 2, GRID_CELLS // 2)
        snake = [start, (start[0]-1, start[1]), (start[0]-2, start[1])]
        direction = RIGHT
        food = random_empty_cell(snake)
        score = 0
        alive = True
        paused = False
        fps = FPS_START
        return snake, direction, food, score, alive, paused, fps

    snake, direction, food, score, alive, paused, fps = reset_game()

    change_dir = direction  # buffer to avoid instant reverse within same tick

    while True:
        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    if direction != DOWN:
                        change_dir = UP
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if direction != UP:
                        change_dir = DOWN
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    if direction != RIGHT:
                        change_dir = LEFT
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    if direction != LEFT:
                        change_dir = RIGHT
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_r:
                    snake, direction, food, score, alive, paused, fps = reset_game()
                    change_dir = direction
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # --- Update ---
        screen.fill(BG)
        draw_grid(screen)

        if alive and not paused:
            direction = change_dir
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = (head_x + dx, head_y + dy)

            # Check collisions with walls
            if not (0 <= new_head[0] < GRID_CELLS and 0 <= new_head[1] < GRID_CELLS):
                alive = False
            # Check collisions with self
            elif new_head in snake:
                alive = False
            else:
                snake.insert(0, new_head)
                if new_head == food:
                    score += 1
                    # speed up every few points
                    if score % FPS_INCREMENT_EVERY == 0:
                        fps = min(30, fps + 1)
                    food = random_empty_cell(snake)
                else:
                    snake.pop()

        # --- Draw snake and food ---
        # body
        for i, cell in enumerate(snake):
            if i == 0:
                draw_rect(screen, SNAKE_HEAD, cell, radius=8)
            else:
                draw_rect(screen, SNAKE_BODY, cell, radius=6)
        # food
        draw_rect(screen, FOOD, food, radius=10)

        # --- UI ---
        render_text(screen, f"Score: {score}", 22, (10, 8))
        render_text(screen, f"High: {high_score}", 22, (WIDTH - 160, 8))
        render_text(screen, "Arrows/WASD to move | P: Pause | R: Restart | Esc: Quit", 18, (10, HEIGHT - 28))

        if not alive:
            # update high score
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            render_text(screen, "GAME OVER", 56, (WIDTH // 2, HEIGHT // 2 - 40), center=True)
            render_text(screen, "Press R to Restart", 28, (WIDTH // 2, HEIGHT // 2 + 10), center=True)

        if paused and alive:
            render_text(screen, "PAUSED", 48, (WIDTH // 2, HEIGHT // 2), center=True)

        pygame.display.flip()
        clock.tick(fps)


if __name__ == "__main__":
    main()
