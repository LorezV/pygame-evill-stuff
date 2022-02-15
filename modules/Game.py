from modules.Player import Player
from modules.Sprites import *
from modules.Drawer import Drawer, ray_casting_walls
from modules.Interface import *
from modules.World import World
from modules.CutScene import *
from random import sample
import pygame


class Game:
    """Основной класс игры. Объединяет в себе почти все остальные классы"""
    def __init__(self):
        self.running = True

        self.screen = pygame.display.set_mode(SIZE)
        self.screen_minimap = pygame.Surface(MAP_RESOLUTION)
        self.world = World(f"data/maps/first_lvl.txt")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('data/fonts/pixels.otf', 72)
        self.font_mini = pygame.font.Font('data/fonts/pixels.otf', 18)
        self.bad_script = pygame.font.Font('data/fonts/bad-script.ttf', 32)
        self.sprites = Sprites(self)
        self.drawer = Drawer(self)
        self.player = Player(self)
        self.menu_picture = pygame.image.load('data/textures/menu.png')
        self.menu_picture = pygame.transform.scale(self.menu_picture,
                                                   (WIDTH, HEIGHT))
        self.win_picture = pygame.image.load('data/textures/win.png')
        self.win_picture = pygame.transform.scale(self.win_picture,
                                                   (WIDTH, HEIGHT))
        self.contols_picture = pygame.image.load('data/textures/controls.png')
        self.contols_picture = pygame.transform.scale(self.contols_picture,
                                                   (WIDTH // 4, HEIGHT // 4))

        self.portal_open = False
        self.pause = False
        self.render_tips = False

        # Init interfaces
        self.labirint_interface = LabirintInterface(self)
        self.pause_interface = GamePauseInterface(self)
        self.menu_interface = MenuInterface(self)
        self.game_over_interface = GameOverInterface(self)
        self.levels_interface = LevelsInterface(self)
        self.player_interface = PlayerInterface(self)
        self.win_interface = WinInterface(self)
        self.tips_interface = Tips(self)

        # Init levels
        self.menu = Menu(self)
        self.loose = Loose(self)
        self.labirint_level = Labirint(self)
        self.planet_level = PlanetLevel(self)
        self.final_level = FinalLevel(self)
        self.win_level = Win(self)

        # Run first level
        self.current_level = None
        self.set_level(self.menu)

        pygame.mixer.music.load('data/music/sc_music.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)

    def set_level(self, level):
        """Инициализация необходимого уровня"""
        self.current_level = level
        if self.current_level.level_name is not None:
            self.world = World(
                f"data/maps/{self.current_level.level_name}.txt")
        self.current_level.init_level()

    def restart(self):
        """Логика кнопки рестарт. Возвращает игру в стартовое состояние."""
        self.player.set_health(100)
        self.player.set_stamina(100)
        self.sprites = Sprites(self)
        for sprite in self.sprites.objects_list:
            sprite.hidden = False
        self.player.notes = [x for x in self.sprites.objects_list if
                             x.flag == "note"]
        self.labirint_interface.update_notes_list()
        self.portal_open = False
        self.set_level(self.labirint_level)
        self.pause = False

    def game_loop(self):
        """Основной игровой цикл"""
        self.current_level.update()
        self.clock.tick(FPS)
        pygame.display.flip()

    def terminate(self):
        """Функция выхода из игры"""
        self.running = False


class Level:
    """Базый класс, для реализации уровня в игре."""
    def __init__(self, game):
        self.game = game
        self.can_pause = False
        self.level_name = None
        self.tips = []

    def update(self, cutscene = None):
        """Обновляет данные уровня каждый кадр. Можно переопределить или расширить."""
        self.check_events(cutscene = cutscene)
        self.game.screen.fill(BLACK)
        if cutscene and not cutscene.is_closed:
            self.game.pause = True
            self.game.current_level.can_pause = False
            cutscene.render()
            return False
        self.game.current_level.can_pause = True
        return True
        
    def spawn_aid_kit(self, coords):
        """Добавление на уровни аптечек"""
        for i in range(3):
            self.game.sprites.objects_list.append(
                AidKit(self.game.sprites.sprite_parametrs['sprite_aid'],
                    (coords[i][0] + 0.98, coords[i][1] + 0.5)))

    def check_events(self, cutscene = None):
        """Метод улавливает события в игре и распределяе логику. Не переопределяется при наследовании."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == ON_MENU_BUTTON_EXIT.type:
                self.game.terminate()
            elif event.type == ON_MENU_BUTTON_START.type:
                self.game.set_level(self.game.labirint_level)
            elif event.type == ON_MENU_BUTTON_RESTART.type:
                self.game.restart()
            elif event.type == ON_MENU_BUTTON_NEXT_LEVEL.type:
                if self.game.current_level.level_name == 'first_lvl':
                    self.game.set_level(self.game.planet_level)
                elif self.game.current_level.level_name == 'second_lvl':
                    self.game.set_level(self.game.final_level)
                elif self.game.current_level.level_name == 'third_lvl':
                    self.game.set_level(self.game.win_level)
                self.game.pause = False
                pygame.event.clear()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if cutscene:
                        cutscene.is_closed = True
                        self.game.pause = False

            if self.game.current_level.can_pause:
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.game.pause = not self.game.pause
                        pygame.mouse.set_visible(self.game.pause)

            if self.game.current_level == self.game.planet_level:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.game.player.weapon.shoot_request()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_r:
                        self.game.player.weapon.reload_request()

            elif self.game.current_level == self.game.labirint_level:
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        if self.game.pause:
                            self.game.sprites.objects_list[0].slender_sound.set_volume(0)
                        else:
                            self.game.sprites.objects_list[0].slender_sound.set_volume(1)

            elif self.game.current_level == self.game.final_level:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.game.player.weapon.shoot_request()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_r:
                        self.game.player.weapon.reload_request()


class Menu(Level):
    """Наследованный от класса Level. Стартовое меню игрока."""
    def __init__(self, game):
        super().__init__(game)

    def init_level(self):
        pygame.mouse.set_visible(True)

    def update(self):
        super().update()
        self.game.screen.fill(BLACK)
        self.game.menu_interface.render()


class Loose(Level):
    """Наследованный от класса Level. Экран поражения."""
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


class Win(Level):
    """Наследованный от класса Level. Экран победы."""
    def __init__(self, game):
        super().__init__(game)

    def init_level(self):
        pygame.mouse.set_visible(True)
        pygame.mixer.quit()
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.load('data/music/rickroll.mp3')
        pygame.mixer.music.play(-1)
        pygame.mouse.set_pos((10, 10))

    def update(self):
        super().update()
        self.game.win_interface.render()


class FinalLevel(Level):
    """Наследованный от класса Level. Уровень с боссом и скелетами."""
    def __init__(self, game):
        super().__init__(game)
        self.can_pause = True
        self.level_name = "third_lvl"
        self.tips = [
            'Уничтожьте всех врагов',
            'Уничтожьте главного монстра',
        ]

    def init_level(self):
        text = 'Уничтожив приспешников, вы решили не останавливаться на достигнутом и отправились на поиски преследователя.\n' \
        'Вскоре вы пришли во вторую часть парка, где встретились со злом лицом к лицу...'
        self.cutscene = CutScene(text, self.game)
        self.game.player.x = PLAYER_SPAWN_POS[0]
        self.game.player.y = PLAYER_SPAWN_POS[1]
        self.game.player.angle = PLAYER_ANGLE
        pygame.mouse.set_visible(False)
        pygame.mixer.music.stop()
        pygame.mixer.music.load('data/music/limit_lvl2.mp3')
        pygame.mixer.music.play(-1)
        self.game.sprites.objects_list.clear()
        self.game.sprites.objects_list = [Slender(self.game.sprites.sprite_parametrs['sprite_slender'], (29.5, 20.5),
                                                  self.game)]
        spawn_coords = list(self.game.world.conj_dict.keys())
        coords = sample(self.game.world.notes_spawn, 3)
        self.spawn_aid_kit(coords)
        for i in sample(spawn_coords, 20):
            self.game.sprites.objects_list.append(
                Skeleton(self.game.sprites.sprite_parametrs['sprite_skeleton'], (i[0] + 0.5, i[1] + 0.5), self.game))

    def update(self):
        cutscene_ended = super().update(cutscene = self.cutscene)
        if not cutscene_ended:
            return
        if not self.game.pause:
            self.game.player.movement()
            for i in range(len(self.game.sprites.objects_list)):
                try:
                    self.game.sprites.objects_list[i].update(self.game.player)
                except Exception:
                    pass
        self.game.drawer.background(self.game.player.ang, sky_texture="sky_2")
        walls, wall_shot = ray_casting_walls(self.game.player, self.game.drawer.textures, self.game.world)
        self.game.drawer.world(walls + [obj.object_locate(self.game.player) for obj in self.game.sprites.objects_list])
        check = self.game.drawer.mini_map(self.game.player, self.game.sprites, True)
        # Win
        if not check:
            pygame.event.clear()
            self.game.set_level(self.game.win_level)
            return
        self.game.levels_interface.render()
        self.game.player_interface.render()
        self.game.tips_interface.render()
        self.game.player.weapon.render([wall_shot, self.game.sprites.sprite_shot])
        if self.game.pause:
            self.game.pause_interface.render()


class PlanetLevel(Level):
    """Наследованный от класса Level. Уровень со скелетами."""
    def __init__(self, game):
        super().__init__(game)
        self.can_pause = True
        self.level_name = "second_lvl"
        self.tips = [
            'Уничьтожьте всех врагов',
        ]

    def init_level(self):
        text = 'Вы смогли сбежать от монстра, однако вас настигли его приспешники.\n' \
       'Во время телепортации у вас в руках оказался дробовик. Вы решили не задавать лишних вопросов и действовать!'
        self.cutscene = CutScene(text, self.game)
        self.game.player.x = PLAYER_SPAWN_POS[0]
        self.game.player.y = PLAYER_SPAWN_POS[1]
        self.game.player.angle = PLAYER_ANGLE
        pygame.mouse.set_visible(False)
        pygame.mixer.music.stop()
        pygame.mixer.music.load('data/music/limit_lvl2.mp3')
        pygame.mixer.music.play(-1)
        self.game.sprites.objects_list.clear()
        spawn_coords = list(self.game.world.conj_dict.keys())
        coords = sample(self.game.world.notes_spawn, 3)
        self.spawn_aid_kit(coords)
        for i in sample(spawn_coords, 30):
            self.game.sprites.objects_list.append(
                Skeleton(self.game.sprites.sprite_parametrs['sprite_skeleton'], (i[0] + 0.5, i[1] + 0.5), self.game))

    def update(self):
        cutscene_ended = super().update(cutscene = self.cutscene)
        if not cutscene_ended:
            return
        if not self.game.pause:
            self.game.player.movement()
            for i in range(len(self.game.sprites.objects_list)):
                try:
                    self.game.sprites.objects_list[i].update(self.game.player)
                except Exception:
                    pass
        self.game.drawer.background(self.game.player.ang, sky_texture="sky_2")
        walls, wall_shot = ray_casting_walls(self.game.player, self.game.drawer.textures, self.game.world)
        self.game.drawer.world(
            walls + [
                obj.object_locate(self.game.player) for
                obj in self.game.sprites.objects_list])
        check = self.game.drawer.mini_map(self.game.player, self.game.sprites, True)
        if not check:
            self.game.set_level(self.game.final_level)
            return
        self.game.levels_interface.render()
        self.game.player_interface.render()
        self.game.player.weapon.render([wall_shot, self.game.sprites.sprite_shot])
        self.game.tips_interface.render()
        if self.game.pause:
            self.game.pause_interface.render()
        if all([i.is_dead for i in self.game.sprites.objects_list]):
            self.game.set_level(self.game.final_level)


class Labirint(Level):
    """Наследованный от класса Level. Уровень с боссом и лабиринтом."""
    def __init__(self, game):
        super().__init__(game)
        self.can_pause = True
        self.level_name = "first_lvl"
        self.tips = [
            'Соберите все записки',
            'Найдите выход',
            'Не дайте монстру убить вас',
        ]
        
    def init_level(self):
        text = 'Ваша машина неожиданно заглохла. Вы проверили всё что могли, но не нашли проблемы.\n' \
        'Отчаявшись, вы отправились в сторону дома, через ближайший парк. Неожиданно за вашей спиной появился забор.\n' \
        'Решительным шагом вы направились в глубину парка, со странной мыслью о сборе записок...'
        self.cutscene = CutScene(text, self.game)
        self.game.player.x = PLAYER_SPAWN_POS[0]
        self.game.player.y = PLAYER_SPAWN_POS[1]
        self.game.player.angle = PLAYER_ANGLE
        pygame.mouse.set_visible(False)
        pygame.mixer.music.load('data/music/gameplay_music.mp3')
        pygame.mixer.music.play(-1)
        coords = sample(self.game.world.notes_spawn, 11)
        self.game.sprites.objects_list = []
        self.game.sprites.objects_list.append(Slender(self.game.sprites.sprite_parametrs['sprite_slender'], (58.5, 38.5), self.game))
        for i in range(8):
            self.game.sprites.objects_list.append(
            Note(self.game.sprites.sprite_parametrs['sprite_note'],
                 (coords[i][0] + 0.98, coords[i][1] + 0.5),
                 [pygame.image.load(
                     f'data/sprites/note/{i + 1}.png').convert_alpha(),
                  pygame.image.load(
                      f"data/sprites/note/angled.png").convert_alpha()], f"{i + 1}",
                 NoteIcon(pygame.image.load(
                     f"data/sprites/note/icons/{i + 1}.png").convert_alpha(),
                          pygame.image.load(
                              f"data/sprites/note/icons/{i + 1}_unfound.png").convert_alpha())))
        self.spawn_aid_kit(coords[::-1])
        self.game.labirint_interface.update_notes_list()

    def update(self):
        cutscene_ended = super().update(cutscene = self.cutscene)
        if not cutscene_ended:
            return
        if not self.game.pause and self.game.current_level == self.game.labirint_level:
            self.game.player.movement()
            self.game.sprites.objects_list[0].update(self.game.player)
        self.game.drawer.background(self.game.player.ang)
        walls, wall_shot = ray_casting_walls(self.game.player, self.game.drawer.textures, self.game.world)
        self.game.drawer.world(walls + [obj.object_locate(self.game.player) for obj in self.game.sprites.objects_list])
        self.game.labirint_interface.render()
        self.game.drawer.interface(self.game.player)
        self.game.tips_interface.render()
        if self.game.pause:
            self.game.pause_interface.render()