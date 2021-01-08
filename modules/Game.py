import sys
from modules.Player import Player
from modules.Sprites import *
from modules.Drawer import Drawer, ray_casting_walls

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        self.screen_minimap = pygame.Surface(MINIMAP_RES)
        self.to_render = self
        self.sprites = Sprites()
        self.clock = pygame.time.Clock()
        self.player = Player(self.sprites)
        self.drawer = Drawer(self.screen, self.screen_minimap)

        pygame.mouse.set_visible(False)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.terminate()

    def game_loop(self):
        self.check_events()
        self.player.movement()
        self.sprites.objects_list[0].action(self.player)

        self.screen.fill(BLACK)
        self.drawer.background(self.player.ang)
        self.drawer.world(ray_casting_walls(self.player, self.drawer.textures) + [obj.object_locate(self.player) for obj in self.sprites.objects_list])
        self.drawer.fps(self.clock)
        self.drawer.mini_map(self.player)
        self.drawer.interface(self.player)

        pygame.display.flip()
        self.clock.tick(FPS)

    def terminate(self):
        pygame.quit()
        sys.exit()