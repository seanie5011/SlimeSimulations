import pygame

pygame.init()

# settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Blank Screen")

# framerate
clock = pygame.time.Clock()
FPS = 60

# MAIN LOOP
run = True
while run:

    clock.tick(FPS)

    for event in pygame.event.get():
        # quitting
        if event.type == pygame.QUIT:
            run = False
        # keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

    pygame.display.update()

pygame.quit()