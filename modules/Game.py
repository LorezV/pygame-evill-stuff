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
        self.font = pygame.font.Font('data/fonts/pixels.otf', 72)
        self.menu_picture = pygame.image.load('data/textures/menu.png')
        pygame.mixer.music.load('data/music/sc_music.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)

    def terminate(self):
        pygame.quit()
        sys.exit()


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
                self.game.terminate()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.game.terminate()
        if keys[pygame.K_0]:
            _gamemanager.set_sceene(_gamemanager.sceenes["labirint"])


class Menu(Sceene, ABC):
    def __init__(self, game):
        super().__init__(game)

    def init_sceene_settings(self):
        pygame.mouse.set_visible(True)

    def game_loop(self):
        self.check_events()
        self.game.screen.blit(self.game.menu_picture, (0, 0),
                              (0, 0, WIDTH, HEIGHT))
        start, exit, startf, exitf = self.draw_buttons()
        pygame.draw.rect(self.game.screen, BLACK, start, border_radius=25,
                         width=10)
        self.game.screen.blit(startf,
                              (start.centerx - 175, start.centery - 40))

        pygame.draw.rect(self.game.screen, BLACK, exit, border_radius=25,
                         width=10)
        self.game.screen.blit(exitf, (exit.centerx - 120, exit.centery - 40))

        label = self.game.font.render('Evill Stuff', 1, (0, 33, 92))
        self.game.screen.blit(label, (280, 20))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if start.collidepoint(mouse_pos):
            pygame.draw.rect(self.game.screen, BLACK, start,
                             border_radius=25)
            self.game.screen.blit(startf,
                                  ((start.centerx - 175, start.centery - 40)))
            if mouse_click[0]:
                pygame.mouse.set_visible(False)
                pygame.mixer.music.stop()
                _gamemanager.set_sceene(_gamemanager.labirint)
        elif exit.collidepoint(mouse_pos):
            pygame.draw.rect(self.game.screen, BLACK, exit, border_radius=25)
            self.game.screen.blit(exitf,
                                  ((exit.centerx - 120, exit.centery - 40)))
            if mouse_click[0]:
                self.game.terminate()

        pygame.display.flip()

    def draw_buttons(self):
        start = self.game.font.render('START', 1, pygame.Color((0, 33, 92)))
        button_start = pygame.Rect(0, 0, 400, 150)
        button_start.center = HALF_WIDTH, HALF_HEIGHT
        exit = self.game.font.render('EXIT', 1, pygame.Color((0, 33, 92)))
        button_exit = pygame.Rect(0, 0, 400, 150)
        button_exit.center = HALF_WIDTH, HALF_HEIGHT + 200
        return button_start, button_exit, start, exit

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
            ray_casting_walls(self.game.player, self.game.drawer.textures) + [
                obj.object_locate(self.game.player) for obj in
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
