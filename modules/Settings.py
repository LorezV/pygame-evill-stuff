import math
import pygame
import ctypes

# Настройки размеров экрана
SIZE = WIDTH, HEIGHT = ctypes.windll.user32.GetSystemMetrics(
    0), ctypes.windll.user32.GetSystemMetrics(1)
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
PENTA_HEIGHT = 5 * HEIGHT
DOUBLE_HEIGHT = HEIGHT * 2
FPS = 60
TILE = 100

# Настройки интерфейса
MARGIN = 10
PADDING = 2
HEALTH_WIDTH, HEALTH_HEIGHT = WIDTH // 5, HEIGHT // 30
HEALTH_TEXT_POS_X, HEALTH_TEXT_POS_Y = MARGIN + HEALTH_WIDTH // 2, MARGIN + HEALTH_HEIGHT // 2

STAMINA_POS_X, STAMINA_POS_Y = MARGIN, HEALTH_HEIGHT + (MARGIN * 2)
STAMINA_WIDTH, STAMINA_HEIGHT = HEALTH_WIDTH, HEALTH_HEIGHT
STAMINA_TEXT_POS_X, STAMINA_TEXT_POS_Y = MARGIN + STAMINA_WIDTH // 2, STAMINA_POS_Y + STAMINA_HEIGHT // 2

MINIMAP_SCALE = 5
MAP_RESOLUTION = (240, 160)
MAP_SCALE = 5 * MINIMAP_SCALE
MAP_TILE = TILE // MAP_SCALE
MAP_POS = (0, HEIGHT - MAP_RESOLUTION[1])

FPS_POS = (WIDTH - 50, 10)

# Настройки rqy-casting
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 300
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 3 * DIST * TILE
SCALE = math.ceil(WIDTH / NUM_RAYS)

# Настройки игрока
PLAYER_SPAWN_POS = (150, 150)
PLAYER_SPEED = 2
PLAYER_SPEED_FAST = 4
PLAYER_ANGLE = 0
SENSITIVITY = 0.002
DOUBLE_PI = math.pi * 2

# Настройки спрайтов
CENTER_RAY = NUM_RAYS // 2 - 1
FAKE_RAYS = 100
FAKE_RAYS_RANGE = NUM_RAYS - 1 + 2 * FAKE_RAYS

# Настройки текстур
TEXTURE_WIDTH = 1200
TEXTURE_HEIGHT = 1200
HALF_TEXTURE_HEIGHT = TEXTURE_HEIGHT // 2
TEXTURE_SCALE = TEXTURE_WIDTH // TILE

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 10, 10)
GREEN = (0, 153, 0)
BLUE = (0, 0, 128)
YELLOW = (255, 204, 0)
DARKGRAY = (36, 37, 41)

MENU_TITLE_COLOR = (255, 200, 0)
MENU_BUTTON_START_COLOR = (255, 10, 10)
MENU_BUTTON_EXIT_COLOR = (0, 33, 92)

# Координаты портала
PORTAL_COORDS = (3255, 120)

# Кастомные события
ON_PLAYER_ENTER_COLLISION = pygame.event.custom_type()
ON_PLAYER_SPAWN = pygame.event.custom_type()

ON_MENU_BUTTON_START = pygame.event.Event(pygame.event.custom_type(),
                                          message="User did pressed START button in menu")
ON_MENU_BUTTON_EXIT = pygame.event.Event(pygame.event.custom_type(),
                                         message="User did pressed EXIT button in menu")
ON_MENU_BUTTON_RESTART = pygame.event.Event(pygame.event.custom_type(),
                                            message="User required restart")
ON_MENU_BUTTON_NEXT_LEVEL = pygame.event.Event(pygame.event.custom_type(),
                                               message="User required next level")
ON_BUTTON_CUTSCENE_SKIP = pygame.event.Event(pygame.event.custom_type(),
                                             message="User required skip cutscene")
