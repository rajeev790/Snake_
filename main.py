import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Load game assets
snake_image = pygame.image.load("assets/images/snake.png")
food_image = pygame.image.load("assets/images/food.png")
background_image = pygame.image.load("assets/images/background.jpg")

# Load sounds
eat_sound = pygame.mixer.Sound("assets/sounds/eat_sound.wav")
game_over_sound = pygame.mixer.Sound("assets/sounds/game_over.wav")
pygame.mixer.music.load("assets/sounds/background_music.mp3")
pygame.mixer.music.play(-1)  # Play background music in loop

# Define colors (Optional, used for texts and other UI elements)
yellow = (255, 255, 102)
red = (213, 50, 80)

# Set screen dimensions
width = 600
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Define the snake and food block size
block_size = 20
snake_speed = 15

# Set clock
clock = pygame.time.Clock()

# Define fonts
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Function to display score
def display_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    screen.blit(value, [0, 0])

# Function to draw the snake using custom image
def draw_snake(snake_body):
    for segment in snake_body:
        screen.blit(snake_image, (segment[0], segment[1]))

# Function to draw food using custom image
def draw_food(x, y):
    screen.blit(food_image, (x, y))

# Function to display game over message
def display_message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [width / 6, height / 3])

# Main game loop
def game_loop():
    game_over = False
    game_close = False

    # Initial snake position
    x = width / 2
    y = height / 2

    # Movement variables
    dx = 0
    dy = 0

    # Snake body and initial length
    snake_body = []
    snake_length = 1

    # Place food at a random position
    food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
    food_y = round(random.randrange(0, height - block_size) / block_size) * block_size

    while not game_over:

        while game_close:
            screen.fill((0, 0, 0))  # Black screen for game over
            display_message("Game Over! Press Q-Quit or C-Play Again", red)
            display_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -block_size
                    dy = 0
                elif event.key == pygame.K_RIGHT:
                    dx = block_size
                    dy = 0
                elif event.key == pygame.K_UP:
                    dx = 0
                    dy = -block_size
                elif event.key == pygame.K_DOWN:
                    dx = 0
                    dy = block_size

        if x >= width or x < 0 or y >= height or y < 0:
            pygame.mixer.Sound.play(game_over_sound)
            game_close = True

        x += dx
        y += dy

        # Optional: Draw background image
        screen.blit(background_image, (0, 0))

        draw_food(food_x, food_y)

        snake_head = [x, y]
        snake_body.append(snake_head)

        if len(snake_body) > snake_length:
            del snake_body[0]

        # Check if the snake collides with itself
        for segment in snake_body[:-1]:
            if segment == snake_head:
                pygame.mixer.Sound.play(game_over_sound)
                game_close = True

        draw_snake(snake_body)
        display_score(snake_length - 1)

        pygame.display.update()

        # Check if the snake eats the food
        if x == food_x and y == food_y:
            pygame.mixer.Sound.play(eat_sound)
            food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
            food_y = round(random.randrange(0, height - block_size) / block_size) * block_size
            snake_length += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Run the game
game_loop()
