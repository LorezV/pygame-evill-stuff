import pygame
import sys
from modules.Player import Player
from modules.Settings import *


def terminate():
    pygame.quit()
    sys.exit()


FPS = 60
SIZE = HEIGHT, WIDTH = 800, 600
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

while True:
    screen.fill(BLUE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    pygame.display.flip()
    clock.tick(FPS)
