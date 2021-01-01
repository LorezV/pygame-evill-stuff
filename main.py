import pygame
import sys
from modules.Settings import *


def terminate():
    pygame.quit()
    sys.exit()


screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

while True:
    screen.fill(BLUE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    pygame.display.flip()
    clock.tick(FPS)
