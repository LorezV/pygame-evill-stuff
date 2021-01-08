import sys
from abc import abstractmethod, ABC
from modules.Player import Player
from modules.Sprites import *
from modules.Drawer import Drawer, ray_casting_walls


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        self.screen_minimap = pygame.Surface(MINIMAP_RES)
        self.sprites = Sprites()
        self.player = Player(self.sprites)
        self.clock = pygame.time.Clock()
        self.drawer = Drawer(self.screen, self.screen_minimap)


class GameManager:
    def __init__(self, game, labirint, menu):
        self.game = game
        self.menu = menu
        self.labirint = labirint

        self.sceenes = {
            "labirint": self.labirint,
            "menu": self.menu,
        }

        _menu.init_sceene_settings()
        self.sceene = self.menu

    def set_sceene(self, sceene):
        sceene.init_sceene_settings()
        self.sceene = sceene

    def update(self):
        self.sceene.game_loop()


class Sceene:
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def init_sceene_settings(self):
        pass

    @abstractmethod
    def game_loop(self):
        pass

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            terminate()
        if keys[pygame.K_0]:
            _gamemanager.set_sceene(_gamemanager.sceenes["labirint"])


class Menu(Sceene, ABC):
    def __init__(self, game):
        super().__init__(game)

    def init_sceene_settings(self):
        pygame.mouse.set_visible(True)

    def game_loop(self):
        self.check_events()
        self.game.screen.fill(BLUE)

        pygame.display.flip()
        self.game.clock.tick(FPS)

    def check_events(self):
        super().check_events()


class Labirint(Sceene, ABC):
    def __init__(self, game):
        super().__init__(game)

    def init_sceene_settings(self):
        pygame.mouse.set_visible(False)

    def game_loop(self):
        self.check_events()
        self.game.player.movement()
        self.game.sprites.objects_list[0].action(self.game.player)

        self.game.screen.fill(BLACK)
        self.game.drawer.background(self.game.player.ang)
        self.game.drawer.world(
            ray_casting_walls(self.game.player, self.game.drawer.textures) + [obj.object_locate(self.game.player) for
                                                                              obj in
                                                                              self.game.sprites.objects_list])
        self.game.drawer.mini_map(self.game.player)
        self.game.drawer.interface(self.game.player)
        self.game.drawer.fps(self.game.clock)

        pygame.display.flip()
        self.game.clock.tick(FPS)

    def check_events(self):
        super().check_events()


_game = Game()
_labirint = Labirint(_game)
_menu = Menu(_game)
_gamemanager = GameManager(_game, _labirint, _menu)


def terminate():
    pygame.quit()
    sys.exit()
