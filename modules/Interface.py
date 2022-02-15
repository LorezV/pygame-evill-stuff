from modules.Settings import *
from modules.Sprites import noteicons_group
from modules.Button import Button
import pygame


class GamePauseInterface:
    """Класс реализует отрисовку игровой паузы."""
    def __init__(self, game):
        self.game = game
        self.menu_sprites_group = pygame.sprite.Group()

        self.restart_button = Button(
            'РЕСТАРТ', ON_MENU_BUTTON_RESTART, self.game)
        self.exit_button = Button("ВЫХОД", ON_MENU_BUTTON_EXIT, self.game)
        self.next_level = Button('ПРОПУСК УРОВНЯ', ON_MENU_BUTTON_NEXT_LEVEL, self.game)
        

        self.initUi()

    def initUi(self):
        self.restart_button.move_bc(HALF_WIDTH, HALF_HEIGHT - 100)
        self.restart_button.color = RED
        self.restart_button.background_color = DARKGRAY
        self.exit_button.move_bc(HALF_WIDTH, HALF_HEIGHT + 200)
        self.exit_button.color = RED
        self.exit_button.background_color = DARKGRAY
        self.next_level.move_bc(HALF_WIDTH, HALF_HEIGHT + 50)
        self.next_level.color = RED
        self.next_level.background_color = DARKGRAY

    def render(self):
        """Метод рендерит на экране элементы интерфейса"""
        self.game.screen.blit(self.game.contols_picture, (WIDTH - self.game.contols_picture.get_width(), HEIGHT - self.game.contols_picture.get_height()))
        pause_text = self.game.font.render('ПАУЗА', 1, RED)
        self.game.screen.blit(pause_text, (HALF_WIDTH - pause_text.get_width() // 2, HALF_HEIGHT - pause_text.get_height() - 300))
        self.restart_button.draw()
        self.exit_button.draw()
        self.next_level.draw()


class WinInterface:
    """Класс реализует отрисовку экрана победы."""
    def __init__(self, game):
        self.game = game

        self.start_button = Button(
            "РЕСТАРТ", ON_MENU_BUTTON_RESTART, self.game)
        self.exit_button = Button("ВЫХОД", ON_MENU_BUTTON_EXIT, self.game)

        self.initUi()

    def initUi(self):
        self.start_button.move_bc(10 + (self.start_button.width // 2), HALF_HEIGHT)
        self.start_button.color = MENU_BUTTON_START_COLOR
        self.exit_button.move_bc(
            10 + (self.exit_button.width // 2), HALF_HEIGHT + 150)
        self.exit_button.color = MENU_BUTTON_EXIT_COLOR

    def render(self):
        """Метод рендерит на экране элементы интерфейса"""
        # Задний фон
        self.game.screen.blit(self.game.win_picture, (0, 0),
                              (0, 0, WIDTH, HEIGHT))

        # Кнопки
        self.start_button.draw()
        self.exit_button.draw()

        # Лого
        label = self.game.font.render('YOU WIN', 1, MENU_TITLE_COLOR)
        self.game.screen.blit(label, (
            10, HEIGHT // 2 - 200))


class MenuInterface:
    """Класс реализует отрисовку игрового меню."""
    def __init__(self, game):
        self.game = game

        self.start_button = Button("НАЧАТЬ", ON_MENU_BUTTON_START, self.game)
        self.exit_button = Button("ВЫХОД", ON_MENU_BUTTON_EXIT, self.game)

        self.initUi()

    def initUi(self):
        self.start_button.move_bc(HALF_WIDTH, HALF_HEIGHT)
        self.start_button.color = MENU_BUTTON_START_COLOR
        self.exit_button.move_bc(HALF_WIDTH, HALF_HEIGHT + 150)
        self.exit_button.color = MENU_BUTTON_EXIT_COLOR

    def render(self):
        """Метод рендерит на экране элементы интерфейса"""
        # Задний фон
        self.game.screen.blit(self.game.menu_picture, (0, 0),
                              (0, 0, WIDTH, HEIGHT))

        # Кнопки
        self.start_button.draw()
        self.exit_button.draw()

        # Лого
        label = self.game.font.render('Evil Stuff', 1, MENU_TITLE_COLOR)
        self.game.screen.blit(label, (
            WIDTH // 2 - label.get_width() // 2, HEIGHT // 2 - 200))
        
        # Управление
        self.game.screen.blit(self.game.contols_picture, (WIDTH - self.game.contols_picture.get_width(), HEIGHT - self.game.contols_picture.get_height()))

class GameOverInterface:
    """Класс реализует отрисовку поражения."""
    def __init__(self, game):
        self.game = game
        self.restart_button = Button(
            "РЕСТАРТ", ON_MENU_BUTTON_RESTART, self.game)
        self.exit_button = Button("ВЫХОД", ON_MENU_BUTTON_EXIT, self.game)
        self.title = self.game.font.render("GAME OVER", 1, YELLOW)

        self.initUi()

    def initUi(self):
        self.restart_button.move_bc(HALF_WIDTH, HALF_HEIGHT)
        self.restart_button.color = RED
        self.restart_button.background_color = YELLOW
        self.exit_button.move_bc(HALF_WIDTH, HALF_HEIGHT + 150)
        self.exit_button.color = RED
        self.exit_button.background_color = YELLOW

    def render(self):
        """Метод рендерит на экране элементы интерфейса"""
        self.game.screen.blit(self.title, (HALF_WIDTH - self.title.get_width() // 2,
                                           HALF_HEIGHT - self.title.get_height() // 2 - 150))
        self.restart_button.draw()
        self.exit_button.draw()


class PlayerInterface:
    """Класс реализует отрисовку интерфейса, связанного с состоянием игрока."""
    def __init__(self, game):
        self.game = game

    def render(self):
        """Метод рендерит на экране элементы интерфейса"""
        ammo_text = self.game.font_mini.render(
            str(self.game.player.weapon.ammo) + " | " + str(self.game.player.weapon.max_ammo), 1, WHITE)
        self.game.screen.blit(
            ammo_text, (WIDTH - ammo_text.get_width(), ammo_text.get_height()))
        self.game.drawer.interface(self.game.player)

    def render_crosshair(self):
        """Метод рендерит на экране прицел оружия"""
        pygame.draw.line(self.game.screen, RED, (HALF_WIDTH - 5,
                         HALF_HEIGHT), (HALF_WIDTH + 5, HALF_HEIGHT), 2)
        pygame.draw.line(self.game.screen, RED, (HALF_WIDTH,
                         HALF_HEIGHT - 5), (HALF_WIDTH, HALF_HEIGHT + 5), 2)


class LabirintInterface:
    """Класс реализует отрисовку элементов интерфейса, только на первом уровне."""
    def __init__(self, game):
        self.game = game

        self.note_group = pygame.sprite.Group()
        self.notes = [note for note in self.game.sprites.objects_list if
                      note.flag == "note"]
        self.update_notes_list()

    def update_notes_list(self):
        """Метод рендерит список записок."""
        count = 0
        for i in range(len(self.game.sprites.objects_list)):
            sprite = self.game.sprites.objects_list[
                len(self.game.sprites.objects_list) - i - 1]
            if sprite.flag == 'note':
                sprite.noteIcon.move((WIDTH - 70) - count * 50, 10)
                count += 1

    def render(self):
        """Метод рендерит на экране элементы интерфейса"""
        noteicons_group.draw(self.game.screen)
        noteicons_group.update()

class LevelsInterface:
    def __init__(self, game):
        self.game = game

    def render(self):
        """Метод рендерит на экране элементы интерфейса"""
        self.game.player_interface.render_crosshair()


class Tips:
    """Класс реализует отрисовку подсказок на клавишу Tab на игровых уровнях."""
    def __init__(self, game):
        self.game = game

    def render(self):
        """Метод рендерит на экране элементы интерфейса"""
        if self.game.render_tips:
            for tip in range(len(self.game.current_level.tips)):
                text = self.game.font_mini.render(
                    self.game.current_level.tips[tip], 1, WHITE)
                self.game.screen.blit(
                    text, (HALF_WIDTH - text.get_width() // 2, 100 + tip * 50))
