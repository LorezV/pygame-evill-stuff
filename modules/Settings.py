import math

# screen settings
SIZE = HEIGHT, WIDTH = 1200, 800
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60
TILE = 100

# ray casting settings
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 120
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 3 * DIST * TILE
SCALE = WIDTH // NUM_RAYS

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (248, 0, 0)
GREEN = (0, 153, 0)
BLUE = (0, 0, 128)
YELLOW = (255, 204, 0)
