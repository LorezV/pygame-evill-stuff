import pygame
import sys
from modules.Player import Player
from modules.Settings import *
from modules.Sprites import *
from modules.Drawer import Drawer


def terminate():
    pygame.quit()
    sys.exit()


pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode(SIZE)
screen_minimap = pygame.Surface((WIDTH // MAP_SCALE, HEIGHT // MAP_SCALE))

sprites = Sprites()
clock = pygame.time.Clock()
player = Player()
drawer = Drawer(screen, screen_minimap)

while True:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    drawer.background(player.ang)
    walls = drawer.ray_casting(player, player.pos, player.ang)
    drawer.world(walls + [obj.object_locate(player, walls) for obj in
                          sprites.objects_list])
    drawer.fps(clock)
    drawer.mini_map(player)
    player.movement()
    drawer.interface(player)
    pygame.display.flip()
    clock.tick(FPS)
