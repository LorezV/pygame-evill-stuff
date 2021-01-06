import pygame
import sys
from modules.Player import Player
from modules.Settings import *
from modules.Sprites import *
from modules.Drawer import Drawer, ray_casting_walls


def terminate():
    pygame.quit()
    sys.exit()


pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode(SIZE)
screen_minimap = pygame.Surface(MINIMAP_RES)

sprites = Sprites()
clock = pygame.time.Clock()
player = Player(sprites)
drawer = Drawer(screen, screen_minimap)

while True:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    drawer.background(player.ang)
    walls = ray_casting_walls(player, drawer.textures)
    drawer.world(walls + [obj.object_locate(player) for obj in
                          sprites.objects_list])
    drawer.fps(clock)
    drawer.mini_map(player)
    player.movement()
    drawer.interface(player)
    pygame.display.flip()
    clock.tick(FPS)
