from pygame.math import Vector2

# Constants
FPS = 15
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
GRID_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 20
MAX_TICKS_WITHOUT_PATH = 1


# Color constants
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BROWN = (151, 87, 43)
PINK = (255, 105, 180) 

# Button's colors
BTN_LIGHT = (170, 170, 170)
BTN_DARK = (100, 100, 100)

# Directional vectors
UP = Vector2(0, -1)
DOWN = Vector2(0, 1)
LEFT = Vector2(-1, 0)
RIGHT = Vector2(1, 0)