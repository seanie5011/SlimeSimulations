import pygame
from pygame.locals import HWSURFACE, DOUBLEBUF, RESIZABLE, VIDEORESIZE
import time

import numpy as np
from scipy.signal import convolve2d

pygame.init()

# settings
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 180

# screen is the backdrop, resizable
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), HWSURFACE|DOUBLEBUF|RESIZABLE)
screen.fill((0, 0, 0))
# zoom screen is where everything is drawn, which in turn is drawn onto screen
zoom_screen = screen.copy()

pygame.display.set_caption("Slime Simulations")

# array to draw from
# must be of type 8-bit unsigned int
draw_array = np.zeros((SCREEN_WIDTH, SCREEN_HEIGHT, 3)).astype('uint8')

# framerate
clock = pygame.time.Clock()
FPS = 60
previous_time = time.time()

# classes
class Agent():
    def __init__(self, x, y, angle, speed=1):
        # set x and y position, and angle
        self.x = x
        self.y = y
        self.angle = angle

        # set speed of movement
        self.speed = speed

    def move(self, dt):
        # move by increasing depending on angle
        self.x += self.speed * np.cos(self.angle * np.pi / 180) * dt
        self.y += self.speed * np.sin(self.angle * np.pi / 180) * dt

        # clamp agent to screen bounds and set on random direction in scope

        # how much to limit angle
        buffer = 45

        # right bound
        if round(self.x) >= SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - 1
            self.angle = np.random.randint(90 + buffer, 270 - buffer)
        # left bound
        if round(self.x) < 0:
            self.x = 0
            self.angle = np.random.randint(-90 + buffer, 90 - buffer)
        # bottom bound
        if round(self.y) >= SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - 1
            self.angle = np.random.randint(-180 + buffer, 0 - buffer)
        # top bound
        if round(self.y) < 0:
            self.y = 0
            self.angle = np.random.randint(0 + buffer, 180 - buffer)

    def draw(self, draw_array):
        # get agents pixel positions
        pixel_x = round(self.x)
        pixel_y = round(self.y)

        # set agents pixel position to white pixel
        draw_array[pixel_x, pixel_y] = [255, 255, 255]

        return draw_array.astype('uint8')

def lerp(a, b, d):
    # linear interpolation between two points, weighted by d
    return a * d + b * (1 - d)

def process_trails(draw_array, fade_speed, diffuse_speed, dt):
    # switch to int for processing
    # have to set array as int while performing operations as it can overflow
    draw_array = draw_array.astype('float64')

    # use a kernel to blur image
    kernel = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]).astype('float64')
    kernel *= 1 / np.sum(kernel)  # normalise
    # loop over all color channels
    for i in range(len(draw_array[0, 0])):
        blur_result = convolve2d(draw_array[:, :, i], kernel, mode='same')
        # lerp between blurred and unblurred
        draw_array[:, :, i] = lerp(draw_array[:, :, i], blur_result, diffuse_speed)

    # fade out trails by going from white to black
    draw_array = np.maximum(0, draw_array - fade_speed * dt)

    # round and make uint8
    draw_array = np.round(draw_array).astype('uint8')

    # return array
    return draw_array

# agents
agents = [Agent(160, 90, i, 20) for i in range(0, 360)]

# fade and blur speed
fade_speed = 30
diffuse_speed = 0.95

# MAIN LOOP

run = True
while run:
    # set deltatime
    dt = time.time() - previous_time
    previous_time = time.time()

    # ACTIONS

    # make canvas from array
    canvas = pygame.surfarray.make_surface(draw_array)

    # trail processing
    draw_array = process_trails(draw_array, fade_speed, diffuse_speed, dt)

    # agent movement and drawing by getting new array
    for agent in agents:
        agent.move(dt)
        draw_array = agent.draw(draw_array)

    # RUNNING

    # set clock tick and display FPS in title
    clock.tick(FPS)
    pygame.display.set_caption(f"Slime Simulations --- FPS: {int(clock.get_fps())}")

    # input and other events
    for event in pygame.event.get():
        # quitting
        if event.type == pygame.QUIT:
            run = False
        # resizing
        if event.type == VIDEORESIZE:
            screen = pygame.display.set_mode(event.size, HWSURFACE|DOUBLEBUF|RESIZABLE)
        # keys
        if event.type == pygame.KEYDOWN:
            # quitting
            if event.key == pygame.K_ESCAPE:
                run = False

    # draw canvas onto zoom screen and display on actual screen by scaling
    zoom_screen.fill((0, 0, 0))
    zoom_screen.blit(canvas, (0, 0))
    screen.blit(pygame.transform.scale(zoom_screen, screen.get_rect().size), (0, 0))
    pygame.display.update()

pygame.quit()