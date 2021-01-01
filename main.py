import pygame
import sys
from modules.Player import Player
from modules.Settings import *
from modules.Drawer import Drawer


def terminate():
    pygame.quit()
    sys.exit()


pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode(SIZE)
screen_minimap = pygame.Surface((WIDTH // MAP_SCALE, HEIGHT // MAP_SCALE))
clock = pygame.time.Clock()
player = Player()
drawer = Drawer(screen, screen_minimap)

while True:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()

    drawer.ray_casting(player.pos, player.ang)
    drawer.fps(clock)
    drawer.mini_map(player)
    player.movement()
    pygame.display.flip()
    clock.tick(FPS)
