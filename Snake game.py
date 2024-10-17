# importing libraries
import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Game settings
snake_speed = 15
window_x = 720
window_y = 480

# Define colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)

# Set up display
pygame.display.set_caption('Snake Game')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS controller
fps = pygame.time.Clock()

# Function to display text on the screen
def display_message(message, color, size, y_offset=0):
    font = pygame.font.SysFont('times new roman', size)
    message_surface = font.render(message, True, color)
    message_rect = message_surface.get_rect(center=(window_x // 2, window_y // 2 + y_offset))
    game_window.blit(message_surface, message_rect)

# Function to show the score
def show_score(color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render(f'Score : {score}', True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)

# Game over function
def game_over():
    game_window.fill(black)
    display_message(f'Your Score is : {score}', red, 50)
    display_message('PRESS R TO RESTART | PRESS E TO EXIT', white, 30, 60)
    pygame.display.flip()
    
    # Wait for user input to either restart or exit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main_game()  # Restart the game
                if event.key == pygame.K_e:
                    pygame.quit()
                    quit()

# Function to wait for any key press to start the game
def wait_for_key_press():
    game_window.fill(black)
    display_message('PRESS ANY KEY TO START GAME', white, 40)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                waiting = False  # Start the game when any key is pressed

# Main game function
def main_game():
    global score  # To track the score
    # Initial snake position and body
    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]

    # Initial fruit position
    fruit_position = [random.randrange(1, (window_x // 10)) * 10, 
                      random.randrange(1, (window_y // 10)) * 10]
    fruit_spawn = True

    # Default direction of the snake
    direction = 'RIGHT'
    change_to = direction

    # Initial score
    score = 0

    # Main game loop
    while True:
        # Handling key events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        # Ensure the snake can't move in the opposite direction instantly
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Move the snake in the current direction
        if direction == 'UP':
            snake_position[1] -= 10
        if direction == 'DOWN':
            snake_position[1] += 10
        if direction == 'LEFT':
            snake_position[0] -= 10
        if direction == 'RIGHT':
            snake_position[0] += 10

        # Snake growing mechanism
        snake_body.insert(0, list(snake_position))
        if snake_position == fruit_position:
            score += 10
            fruit_spawn = False
        else:
            snake_body.pop()

        # Spawning new fruit
        if not fruit_spawn:
            fruit_position = [random.randrange(1, (window_x // 10)) * 10, 
                              random.randrange(1, (window_y // 10)) * 10]
        fruit_spawn = True

        # Fill the game window with black background
        game_window.fill(black)

        # Draw the snake and fruit
        for pos in snake_body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

        # Check for collisions with the boundaries
        if (snake_position[0] < 0 or snake_position[0] > window_x-10 or
                snake_position[1] < 0 or snake_position[1] > window_y-10):
            game_over()

        # Check for collisions with itself
        for block in snake_body[1:]:
            if snake_position == block:
                game_over()

        # Display score
        show_score(white, 'times new roman', 20)

        # Refresh the game screen
        pygame.display.update()

        # Control the frame rate
        fps.tick(snake_speed)

# Start the game with the 'PRESS ANY KEY TO START GAME' screen
wait_for_key_press()
main_game()