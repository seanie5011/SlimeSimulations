import numpy as np
from scipy.signal import convolve2d

# functions

def lerp(a, b, d):
    '''
    Performs linear interpolation between a and b, returning the midpoint weighted by d.
    '''

    # linear interpolation between two points, weighted by d
    return a * d + b * (1 - d)

def process_trails(draw_array, fade_speed, diffuse_speed, dt):
    '''
    Processes a draw_array to perform blurring and fading on trails.
    '''

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

# classes

class Agent():
    def __init__(self, x, y, angle, speed=1, SCREEN_WIDTH=320, SCREEN_HEIGHT=180):
        # set x and y position, and angle
        self.x = x
        self.y = y
        self.angle = angle

        # settings
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT

        # set speed of movement
        self.speed = speed

    def move(self, dt):
        '''
        Move in a certain direction then clamp bounds. When agent reaches bounds, \
        move in random direction within range.
        '''

        # move by increasing depending on angle
        self.x += self.speed * np.cos(self.angle * np.pi / 180) * dt
        self.y += self.speed * np.sin(self.angle * np.pi / 180) * dt

        # clamp agent to screen bounds and set on random direction in scope

        # how much to limit angle
        buffer = 45

        # right bound
        if round(self.x) >= self.SCREEN_WIDTH:
            self.x = self.SCREEN_WIDTH - 1
            self.angle = np.random.randint(90 + buffer, 270 - buffer)
        # left bound
        if round(self.x) < 0:
            self.x = 0
            self.angle = np.random.randint(-90 + buffer, 90 - buffer)
        # bottom bound
        if round(self.y) >= self.SCREEN_HEIGHT:
            self.y = self.SCREEN_HEIGHT - 1
            self.angle = np.random.randint(-180 + buffer, 0 - buffer)
        # top bound
        if round(self.y) < 0:
            self.y = 0
            self.angle = np.random.randint(0 + buffer, 180 - buffer)

    def draw(self, draw_array):
        '''
        Draw by setting agents current pixel position to a white pixel.
        '''

        # get agents pixel positions
        pixel_x = round(self.x)
        pixel_y = round(self.y)

        # set agents pixel position to white pixel
        draw_array[pixel_x, pixel_y] = [255, 255, 255]

        return draw_array.astype('uint8')