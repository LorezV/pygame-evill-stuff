import pygame
import sys
from modules.Player import Player
from modules.Settings import *
from modules.Drawer import Drawer


def terminate():
    pygame.quit()
    sys.exit()


screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
player = Player()
drawer = Drawer(screen)

while True:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    # player.draw(screen)
    drawer.ray_casting(player.pos, player.ang)
    player.movement()
    pygame.display.flip()
    clock.tick(FPS)
