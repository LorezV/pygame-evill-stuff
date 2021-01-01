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
player = Player()

while True:
    screen.fill(BLUE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()

    player.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
