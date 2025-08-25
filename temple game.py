# Temple Run Style Infinite Runner (2D) in Python (pygame)
# Install pygame first: pip install pygame

import pygame
import random
import sys

# --- Game Settings ---
WIDTH, HEIGHT = 800, 400
FPS = 60
GRAVITY = 0.8
JUMP_POWER = -15

# Colors
BG_COLOR = (30, 30, 30)
PLAYER_COLOR = (0, 200, 255)
OBSTACLE_COLOR = (255, 80, 80)
TEXT_COLOR = (240, 240, 240)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Temple Run Style Game - Python")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 30, bold=True)

# --- Player ---
class Player:
    def __init__(self):
        self.width, self.height = 40, 60
        self.x = 80
        self.y = HEIGHT - self.height - 40
        self.vel_y = 0
        self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_POWER
            self.on_ground = False

    def update(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y
        if self.y >= HEIGHT - self.height - 40:
            self.y = HEIGHT - self.height - 40
            self.vel_y = 0
            self.on_ground = True

    def draw(self):
        pygame.draw.rect(screen, PLAYER_COLOR, (self.x, self.y, self.width, self.height), border_radius=8)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# --- Obstacle ---
class Obstacle:
    def __init__(self):
        self.width = 30
        self.height = random.choice([40, 60, 80])
        self.x = WIDTH + 20
        self.y = HEIGHT - self.height - 40
        self.speed = 8

    def update(self):
        self.x -= self.speed

    def draw(self):
        pygame.draw.rect(screen, OBSTACLE_COLOR, (self.x, self.y, self.width, self.height), border_radius=4)

    def off_screen(self):
        return self.x < -self.width

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# --- Game Loop ---
def main():
    player = Player()
    obstacles = []
    score = 0
    high_score = 0
    obstacle_timer = 0
    running = True
    alive = True

    while running:
        screen.fill(BG_COLOR)

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if alive:
                    if event.key == pygame.K_SPACE:
                        player.jump()
                else:
                    if event.key == pygame.K_r:
                        return main()  # restart game

        # --- Update ---
        if alive:
            player.update()
            obstacle_timer += 1
            if obstacle_timer > 80:
                obstacles.append(Obstacle())
                obstacle_timer = 0

            for obs in list(obstacles):
                obs.update()
                if obs.off_screen():
                    obstacles.remove(obs)
                    score += 1

                if player.get_rect().colliderect(obs.get_rect()):
                    alive = False
                    high_score = max(high_score, score)

        # --- Draw ---
        # ground line
        pygame.draw.line(screen, (200, 200, 200), (0, HEIGHT - 40), (WIDTH, HEIGHT - 40), 3)

        player.draw()
        for obs in obstacles:
            obs.draw()

        # Score
        score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
        screen.blit(score_text, (10, 10))

        # Game over screen
        if not alive:
            over_text = font.render("GAME OVER - Press R to Restart", True, (255, 200, 200))
            screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 20))
            hs_text = font.render(f"High Score: {high_score}", True, (200, 200, 0))
            screen.blit(hs_text, (WIDTH//2 - hs_text.get_width()//2, HEIGHT//2 + 20))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
