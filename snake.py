# Import related modules
import random
import pygame
import sys

from pygame.locals import *


snake_speed = 8  # The Speed of Snake
windows_width = 800
windows_height = 600  # Size of Game Window
cell_size = 20
# Snake body square size, note that body size must be divisible by window length and width

# Initialization area
# Since our snakes are of size, the actual size of the map is relative to the size of the snake.

map_width = int(windows_width / cell_size)
map_height = int(windows_height / cell_size)

# define color
white = (255, 255, 255)
black = (0, 0, 0)
gray = (230, 230, 230)
dark_gray = (40, 40, 40)
DARKGreen = (0, 155, 0)
Green = (0, 255, 0)
Red = (255, 0, 0)
blue = (0, 0, 255)
dark_blue = (0, 0, 139)


BG_COLOR = black  # Game background color

# Define direction
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

HEAD = 0  # Snake head subscript

# Main function


def main():
    pygame.init()  # Module Initialization
    snake_speed_clock = pygame.time.Clock()  # Create PyGame Clock Object
    screen = pygame.display.set_mode((windows_width, windows_height))
    screen.fill(white)

    pygame.display.set_caption("Python snake game")  # Set title
    show_start_info(screen)               # Welcome information
    while True:
        running_game(screen, snake_speed_clock)
        show_gameover_info(screen)


# Game Operating Subject


def running_game(screen, snake_speed_clock):
    startx = random.randint(3, map_width - 8)  # Starting position
    starty = random.randint(3, map_height - 8)
    snake_coords = [{'x': startx, 'y': starty},
                    {'x': startx - 1, 'y': starty},
                    {'x': startx - 2, 'y': starty}]  # Initial snake

    direction = RIGHT       # Move right at first

    food = get_random_location()     # Random physical location

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        move_snake(direction, snake_coords)  # move snake

        ret = snake_is_alive(snake_coords)
        if not ret:
            break  # The snake is dead, game over
        snake_is_eat_food(snake_coords, food)  # Judging whether snakes have eaten food

        screen.fill(BG_COLOR)
        # draw_grid(screen)
        draw_snake(screen, snake_coords)
        draw_food(screen, food)
        draw_score(screen, len(snake_coords) - 3)
        pygame.display.update()
        snake_speed_clock.tick(snake_speed)  # control fps

# Draw food


def draw_food(screen, food):
    x = food['x'] * cell_size
    y = food['y'] * cell_size
    appleRect = pygame.Rect(x, y, cell_size, cell_size)
    pygame.draw.rect(screen, Red, appleRect)

#  draw snake


def draw_snake(screen, snake_coords):
    for coord in snake_coords:
        x = coord['x'] * cell_size
        y = coord['y'] * cell_size
        wormSegmentRect = pygame.Rect(x, y, cell_size, cell_size)
        pygame.draw.rect(screen, dark_blue, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, cell_size - 8, cell_size - 8)
        pygame.draw.rect(screen, white, wormInnerSegmentRect)

# The second layer of bright green inside the snake's body


# draw grid(Optional)


def draw_grid(screen):
    for x in range(0, windows_width, cell_size):  # draw horizontal lines
        pygame.draw.line(screen, dark_gray, (x, 0), (x, windows_height))
    for y in range(0, windows_height, cell_size):  # draw vertical lines
        pygame.draw.line(screen, dark_gray, (0, y), (windows_width, y))

# move snake


def move_snake(direction, snake_coords):
    if direction == UP:
        newHead = {'x': snake_coords[HEAD]['x'], 'y': snake_coords[HEAD]['y'] - 1}
    elif direction == DOWN:
        newHead = {'x': snake_coords[HEAD]['x'], 'y': snake_coords[HEAD]['y'] + 1}
    elif direction == LEFT:
        newHead = {'x': snake_coords[HEAD]['x'] - 1, 'y': snake_coords[HEAD]['y']}
    elif direction == RIGHT:
        newHead = {'x': snake_coords[HEAD]['x'] + 1, 'y': snake_coords[HEAD]['y']}

    snake_coords.insert(0, newHead)

# 判断蛇死了没


def snake_is_alive(snake_coords):
    tag = True
    if snake_coords[HEAD]['x'] == -1 \
            or snake_coords[HEAD]['x'] == map_width \
            or snake_coords[HEAD]['y'] == -1 \
            or snake_coords[HEAD]['y'] == map_height:
        tag = False  # Snake hitting a wall
    for snake_body in snake_coords[1:]:
        if snake_body['x'] == snake_coords[HEAD]['x'] and snake_body['y'] == snake_coords[HEAD]['y']:
            tag = False  # The snake touched itself.
    return tag

# Judging whether a snake eats food


def snake_is_eat_food(snake_coords, food):
    if snake_coords[HEAD]['x'] == food['x'] and snake_coords[HEAD]['y'] == food['y']:
        food['x'] = random.randint(0, map_width - 1)
        food['y'] = random.randint(0, map_height - 1)  # Restructuring Food Location
    else:
        del snake_coords[-1]
        # If the snake has not eaten the food, it moves forward, and the tail is deleted

# Food random generation


def get_random_location():
    return {'x': random.randint(0, map_width - 1), 'y': random.randint(0, map_height - 1)}

# Start Information Display


def show_start_info(screen):
    font = pygame.font.Font('myfont.ttf', 40)
    tip = font.render('Press any key to start the game~~~', True, (65, 105, 225))
    gamestart = pygame.image.load('gamestart.jpg')
    screen.blit(gamestart, (140, 30))
    screen.blit(tip, (100, 550))
    pygame.display.update()

    while True:  # Keyboard listening events
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()     # Termination procedure
            elif event.type == KEYDOWN:
                if (event.key == K_ESCAPE):  # Termination procedure
                    terminate()  # Termination procedure
                else:
                    return  # End this function and start the game

# Game End Information Display


def show_gameover_info(screen):
    font = pygame.font.Font('myfont.ttf', 40)
    tip1 = font.render('Press Q or ESC to exit the game ~', True, (65, 105, 225))
    tip2 = font.render('Press  any key to restart the game~', True, (65, 105, 225))
    gamestart = pygame.image.load('gameover.jpg')
    screen.blit(gamestart, (60, 0))
    screen.blit(tip1, (50, 450))
    screen.blit(tip2, (50, 500))
    pygame.display.update()

    while True:  # Keyboard listening events
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()     # Termination procedure
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:  # Termination procedure
                    terminate()  # Termination procedure
                else:
                    return  # End this function and restart the game

# draw score


def draw_score(screen, score):
    font = pygame.font.Font('myfont.ttf', 30)
    scoreSurf = font.render('Score:%s' % score, True, Green)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (windows_width - 120, 10)
    screen.blit(scoreSurf, scoreRect)

# Program termination


def terminate():
    pygame.quit()
    sys.exit()


main()
