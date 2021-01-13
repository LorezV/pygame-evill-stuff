from modules.Player import Player
from modules.Sprites import *
from modules.Drawer import Drawer, ray_casting_walls
from modules.Interface import *


class Game:
    def __init__(self):
        self.running = True

        self.screen = pygame.display.set_mode(SIZE)
        self.screen_minimap = pygame.Surface(MAP_RESOLUTION)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('data/fonts/pixels.otf', 72)
        self.font_mini = pygame.font.Font('data/fonts/pixels.otf', 18)
        self.sprites = Sprites()
        self.drawer = Drawer(self)
        self.player = Player(self)
        self.menu_picture = pygame.image.load('data/textures/menu.png')
        self.menu_picture = pygame.transform.scale(self.menu_picture,
                                                   (WIDTH, HEIGHT))

        self.portal_open = False
        self.pause = False

        # Init interfaces
        self.labirint_interface = LabirintInterface(self)
        self.pause_interface = GamePauseInterface(self)
        self.menu_interface = MenuInterface(self)
        self.game_over_interface = GameOverInterface(self)
        self.planet_interface = PlanetLevelInterface(self)

        # Init levels
        self.menu = Menu(self)
        self.loose = Loose(self)
        self.labirint_level = Labirint(self)
        self.planet_level = PlanetLevel(self)

        # Run first level
        self.current_level = None
        self.set_level(self.menu)

        pygame.mixer.music.load('data/music/sc_music.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)

    def set_level(self, level):
        self.current_level = level
        self.current_level.init_level()

    def restart(self):
        self.player.x = PLAYER_SPAWN_POS[0]
        self.player.y = PLAYER_SPAWN_POS[1]
        self.player.angle = PLAYER_ANGLE
        self.player.set_health(100)
        self.player.set_stamina(100)
        self.sprites = Sprites()
        for sprite in self.sprites.objects_list:
            sprite.hidden = False
        self.player.notes = [x for x in self.sprites.objects_list if x.flag == "note"]
        self.labirint_interface.update_notes_list()
        self.portal_open = False
        self.set_level(self.labirint_level)
        self.pause = False

    def game_loop(self):
        self.current_level.update()
        self.clock.tick(FPS)
        pygame.display.flip()

    def terminate(self):
        self.running = False


class Level:
    def __init__(self, game):
        self.game = game

    def update(self):
        self.check_events()
        self.game.screen.fill(BLACK)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == ON_MENU_BUTTON_EXIT.type:
                self.game.terminate()
            elif event.type == ON_MENU_BUTTON_START.type:
                self.game.set_level(self.game.labirint_level)
            elif event.type == ON_MENU_BUTTON_RESTART.type:
                self.game.restart()

            if self.game.current_level == self.game.labirint_level:
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.game.pause = not self.game.pause
                        pygame.mouse.set_visible(self.game.pause)
                    elif event.key == pygame.K_SPACE:
                        self.game.player.set_health(0)


class Menu(Level):
    def __init__(self, game):
        super().__init__(game)

    def init_level(self):
        pygame.mouse.set_visible(True)

    def update(self):
        super().update()
        self.game.screen.fill(BLACK)
        self.game.menu_interface.render()


class Loose(Level):
    def __init__(self, game):
        super().__init__(game)

    def init_level(self):
        pygame.mouse.set_visible(True)
        pygame.mixer.quit()
        pygame.mixer.init()
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.load('data/music/lose_music.mp3')
        pygame.mixer.music.play(-1)

    def update(self):
        super().update()
        self.game.game_over_interface.render()


class PlanetLevel(Level):
    def __init__(self, game):
        super().__init__(game)

    def init_level(self):
        pygame.mouse.set_visible(True)
        pygame.mixer.quit()
        pygame.mixer.init()
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.load('data/music/to_be_continued.mp3')
        pygame.mixer.music.play(-1)

    def update(self):
        super().update()
        self.game.planet_interface.render()


class Labirint(Level):
    def __init__(self, game):
        super().__init__(game)
        self.labirint_interface = self.game.labirint_interface

    def init_level(self):
        pygame.mouse.set_visible(False)
        pygame.mixer.music.load('data/music/gameplay_music.mp3')
        pygame.mixer.music.play(-1)

    def update(self):
        super().update()
        if not self.game.pause:
            self.game.player.movement()
            self.game.sprites.objects_list[0].action(self.game.player)
        self.game.drawer.background(self.game.player.ang)
        self.game.drawer.world(
            ray_casting_walls(self.game.player, self.game.drawer.textures) + [
                obj.object_locate(self.game.player) for obj in
                self.game.sprites.objects_list])
        self.game.drawer.mini_map(self.game.player, self.game.sprites)
        self.game.drawer.fps(self.game.clock)
        self.labirint_interface.render()
        if self.game.pause:
            self.game.pause_interface.render()
