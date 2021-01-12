import sys
from abc import abstractmethod, ABC
from modules.Player import Player
from modules.Sprites import *
from modules.Drawer import Drawer, ray_casting_walls


class Game:
    def __init__(self, gamemanager):
        pygame.init()
        self.gamemanager = gamemanager
        self.screen = pygame.display.set_mode(SIZE)
        self.screen_minimap = pygame.Surface(MAP_RESOLUTION)
        self.sprites = Sprites()
        self.drawer = Drawer(self.screen, self.screen_minimap)
        self.player = Player(self.sprites, self.gamemanager, self.drawer)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('data/fonts/pixels.otf', 72)
        self.menu_picture = pygame.image.load('data/textures/menu.png')
        self.menu_picture = pygame.transform.scale(self.menu_picture,
                                                   (WIDTH, HEIGHT))
        pygame.mixer.music.load('data/music/sc_music.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)

    def terminate(self):
        pygame.quit()
        sys.exit()


class GameManager:
    def __init__(self):
        pass

    def init_gamemanager(self, game, labirint, menu, lose, level_two):
        self.game = game
        self.menu = menu
        self.labirint = labirint
        self.level_two = level_two
        self.lose = lose

        self.portal_open = False

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


class Menu(Sceene, ABC):
    def __init__(self, game):
        super().__init__(game)
        self.menu_sprites_group = pygame.sprite.Group()

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
        self.game.screen.blit(label, (
            WIDTH // 2 - label.get_width() // 2, HEIGHT // 2 - 200))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if start.collidepoint(mouse_pos):
            pygame.draw.rect(self.game.screen, BLACK, start,
                             border_radius=25)
            self.game.screen.blit(startf,
                                  (start.centerx - 175, start.centery - 40))
            if mouse_click[0]:
                pygame.mouse.set_visible(False)
                pygame.mixer.music.stop()
                gamemanager.set_sceene(gamemanager.labirint)
        elif exit.collidepoint(mouse_pos):
            pygame.draw.rect(self.game.screen, BLACK, exit, border_radius=25)
            self.game.screen.blit(exitf,
                                  (exit.centerx - 120, exit.centery - 40))
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


class Lose(Sceene, ABC):
    def __init__(self, game):
        super().__init__(game)
        self.lose_sprites_group = pygame.sprite.Group()

    def init_sceene_settings(self):
        pygame.mouse.set_visible(True)
        pygame.mixer.quit()
        pygame.mixer.init()
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.load('data/music/lose_music.mp3')
        pygame.mixer.music.play(-1)

    def game_loop(self):
        self.check_events()
        self.game.screen.fill(BLACK)
        restart, restartf = self.draw_buttons()

        pygame.draw.rect(self.game.screen, YELLOW, restart, border_radius=25,
                         width=10)
        self.game.screen.blit(restartf,
                              (restart.centerx - 120, restart.centery - 40))

        label = self.game.font.render('GAME OVER', 1, RED)
        self.game.screen.blit(label, (
            WIDTH // 2 - label.get_width() // 2, HEIGHT // 2 - 200))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if restart.collidepoint(mouse_pos):
            pygame.draw.rect(self.game.screen, YELLOW, restart,
                             border_radius=25)
            self.game.screen.blit(restartf,
                                  (
                                      restart.centerx - 120, restart.centery + 120))
            if mouse_click[0]:
                self.game.player.restart()
        pygame.display.flip()

    def draw_buttons(self):
        restart = self.game.font.render('RESTART', 1,
                                        pygame.Color((0, 33, 92)))
        button_restart = pygame.Rect(0, 0, 400, 150)
        button_restart.center = HALF_WIDTH, HALF_HEIGHT + 200
        return button_restart, restart

    def check_events(self):
        super().check_events()


class LevelTwo(Sceene, ABC):
    def __init__(self, game):
        super().__init__(game)

    def init_sceene_settings(self):
        pygame.mouse.set_visible(True)
        pygame.mixer.quit()
        pygame.mixer.init()
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.load('data/music/to_be_continued.mp3')
        pygame.mixer.music.play(-1)

    def game_loop(self):
        self.check_events()
        self.game.screen.fill(BLACK)
        background_image = pygame.image.load("data/textures/sky.png")
        background_image = pygame.transform.scale(background_image,
                                                  (WIDTH, HEIGHT))
        self.game.screen.blit(background_image, (0, 0))
        text_render = self.game.font.render("To be continue", 1, WHITE)
        self.game.screen.blit(text_render,
                              (100, HEIGHT - 100 - text_render.get_height()))
        pygame.display.flip()

    def check_events(self):
        super().check_events()


class Labirint(Sceene, ABC):
    def __init__(self, game, labirint_interface):
        super().__init__(game)
        self.labirint_interface = labirint_interface
        self.pause = False

    def init_sceene_settings(self):
        pygame.mouse.set_visible(False)
        pygame.mixer.music.load('data/music/gameplay_music.mp3')
        pygame.mixer.music.play(-1)

    def game_loop(self):
        self.check_events()
        if not self.pause:
            self.game.player.movement()
            self.game.sprites.objects_list[0].action(self.game.player)

            self.game.screen.fill(BLACK)
            self.game.drawer.background(self.game.player.ang)
            self.game.drawer.world(
                ray_casting_walls(self.game.player, self.game.drawer.textures) + [
                    obj.object_locate(self.game.player) for obj in
                    self.game.sprites.objects_list])
            self.game.drawer.mini_map(self.game.player, _game.sprites)
            self.game.drawer.interface(self.game.player)
            self.labirint_interface.render()
            self.game.drawer.fps(self.game.clock)
        else:
            label = self.game.font.render('PAUSE', 1, RED)
            self.game.screen.blit(label, (
                WIDTH // 2 - label.get_width() // 2, HEIGHT // 2 - 200))

        pygame.display.flip()
        self.game.clock.tick(FPS)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.pause = not self.pause
            elif event.type == pygame.QUIT:
                self.game.terminate()


class LabirintInterface():
    def __init__(self):
        self.note_group = pygame.sprite.Group()
        self.notes = [note for note in _game.sprites.objects_list if
                      note.flag == "note"]

        for i in range(len(_game.sprites.objects_list)):
            sprite = _game.sprites.objects_list[
                len(_game.sprites.objects_list) - i - 1]
            if sprite.flag == 'note':
                sprite.noteIcon.move((WIDTH - 70) - i * 50, 10)

    def render(self):
        noteicons_group.draw(_game.screen)
        noteicons_group.update()


gamemanager = GameManager()
_game = Game(gamemanager)
_labirint_interface = LabirintInterface()
_labirint = Labirint(_game, _labirint_interface)
_level_two = LevelTwo(_game)
_menu = Menu(_game)
_lose = Lose(_game)
gamemanager.init_gamemanager(_game, _labirint, _menu, _lose, _level_two)
