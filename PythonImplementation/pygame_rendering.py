import pygame
from pygame.locals import HWSURFACE, DOUBLEBUF, RESIZABLE, VIDEORESIZE
import time

from pygame_agent import lerp, process_trails, Agent
import numpy as np

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

# framerate
clock = pygame.time.Clock()
FPS = 60
previous_time = time.time()

# array to draw from
# must be of type 8-bit unsigned int
draw_array = np.zeros((SCREEN_WIDTH, SCREEN_HEIGHT, 3)).astype('uint8')

# agents
agents = [Agent(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, i, 20, SCREEN_WIDTH, SCREEN_HEIGHT) for i in range(0, 360)]

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