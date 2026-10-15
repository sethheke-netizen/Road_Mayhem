import pygame
import random
import sys
import os

pygame.init()
WIDTH = 500
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Road Mayhem")
clock = pygame.time.Clock()
WHITE = (255, 255, 255)
RED = (220, 30, 30)
BLUE = (30, 100, 220)
GREY = (30, 150, 50)
GREEN = (0, 0, 0)
YELLOW = (240, 200, 30)
BLACK = (20, 20, 20)
LIGHT_BROWN = (120, 120, 120)
road_left = 75
road_right = 425
WIN_SCORE = 100
car_width = 50
car_height = 90
car_x = WIDTH // 2 - 25
car_y = HEIGHT - 120
car_speed = 16 

enemy_width = 50
enemy_height = 90
enemy_x = random.randint(road_left, road_right - enemy_width)
enemy_y = -100
enemy_speed = 4
enemy2_x = random.randint(road_left, road_right - enemy_width)
enemy2_y = -400
enemy2_speed = 4
obstacle_width = 40
obstacle_height = 40
obstacle_x = random.randint(road_left, road_right - obstacle_width)
obstacle_y = -600
obstacle_speed = 4
score = 0
high_score = 0
game_over = False
won = False
running = True
high_score_file = "highscore.txt"
if os.path.exists(high_score_file):
    with open(high_score_file, "r") as file:
        try:
            high_score = int(file.read())
        except ValueError:
            high_score = 0

font = pygame.font.Font(None, 40)
game_font = pygame.font.Font(None, 70)
def draw_car(x, y, color):
    pygame.draw.rect(screen, color, (x, y, car_width, car_height), border_radius=8)
    pygame.draw.rect(screen, BLACK, (x + 10, y + 10, 30, 25))
    pygame.draw.rect(screen, BLACK, (x - 5, y + 15, 8, 20))
    pygame.draw.rect(screen, BLACK, (x + 47, y + 15, 8, 20))
    pygame.draw.rect(screen, BLACK, (x - 5, y + 55, 8, 20))
    pygame.draw.rect(screen, BLACK, (x + 47, y + 55, 8, 20))

def draw_obstacle(x, y):
    pygame.draw.rect(screen, YELLOW, (x, y, obstacle_width, obstacle_height))
    pygame.draw.line(screen, BLACK, (x, y), (x + 40, y + 40), 5)
    pygame.draw.line(screen, BLACK, (x + 40, y), (x, y + 40), 5)

def draw_rail(x):
    pygame.draw.rect(screen, LIGHT_BROWN, (x, 0, 10, HEIGHT))
    pygame.draw.rect(screen, WHITE, (x, 0, 10, HEIGHT), 2)
    for y in range(0, HEIGHT, 70):
        pygame.draw.rect(screen, LIGHT_BROWN, (x - 5, y, 20, 8))
        pygame.draw.rect(screen, WHITE, (x - 5, y, 20, 8), 2)

def save_high_score():
    with open(high_score_file, "w") as file:
        file.write(str(high_score))

def reset_game():
    global car_x, enemy_x, enemy_y, enemy_speed
    global enemy2_x, enemy2_y, enemy2_speed
    global obstacle_x, obstacle_y, obstacle_speed
    global score, game_over, won
    car_x = WIDTH // 2 - car_width // 2
    enemy_x = random.randint(road_left, road_right - enemy_width)
    enemy_y = -100
    enemy_speed = 5
    enemy2_x = random.randint(road_left, road_right - enemy_width)
    enemy2_y = -400
    enemy2_speed = 5
    obstacle_x = random.randint(road_left, road_right - obstacle_width)
    obstacle_y = -600
    obstacle_speed = 5
    score = 0
    game_over = False
    won = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r and (game_over or won):
                reset_game()
    keys = pygame.key.get_pressed()
    if not game_over and not won:
        if keys[pygame.K_LEFT]:
            car_x -= car_speed
        if keys[pygame.K_RIGHT]:
            car_x += car_speed
        if car_x < road_left:
            car_x = road_left
        if car_x > road_right - car_width:
            car_x = road_right - car_width
        enemy_y += enemy_speed
        enemy2_y += enemy2_speed
        obstacle_y += obstacle_speed
        if enemy_y > HEIGHT:
            enemy_y = -100
            enemy_x = random.randint(road_left, road_right - enemy_width)
            score += 1
        if enemy2_y > HEIGHT:
            enemy2_y = -300
            enemy2_x = random.randint(road_left, road_right - enemy_width)
            score += 1
        if obstacle_y > HEIGHT:
            obstacle_y = -500
            obstacle_x = random.randint(road_left, road_right - obstacle_width)
            score += 1
        player = pygame.Rect(car_x, car_y, car_width, car_height)
        enemy = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
        enemy2 = pygame.Rect(enemy2_x, enemy2_y, enemy_width, enemy_height)
        obstacle = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)
        if player.colliderect(enemy) or player.colliderect(enemy2):
            game_over = True
        if player.colliderect(obstacle):
            game_over = True
        if score > high_score:
            high_score = score
            save_high_score()
        if score >= WIN_SCORE:
            won = True
        if score > 0 and score % 5 == 0:
            enemy_speed = 5 + score // 5
            enemy2_speed = 5 + score // 5
            obstacle_speed = 5 + score // 5
    screen.fill(GREY)
    pygame.draw.rect(screen, GREEN, (road_left, 0, road_right - road_left, HEIGHT))
    draw_rail(road_left - 15)
    draw_rail(road_right - 7)
    for y in range(0, HEIGHT, 90):
        pygame.draw.rect(screen, YELLOW, (WIDTH // 2 - 5, y, 10, 40))
    draw_car(car_x, car_y, RED)
    draw_car(enemy_x, enemy_y, BLUE)
    draw_car(enemy2_x, enemy2_y, BLUE)
    draw_obstacle(obstacle_x, obstacle_y)
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    screen.blit(font.render(f"High Score: {high_score}", True, WHITE), (10, 45))
    if game_over:
        text = game_font.render("GAME OVER", True, WHITE)
        restart = font.render("Press R to restart", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 60))
        screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT // 2 + 20))
    if won:
        text = game_font.render("YOU WIN!", True, YELLOW)
        message = font.render("You reached 100 points!", True, WHITE)
        restart = font.render("Press R to play again", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 90))
        screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2))
        screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit() 