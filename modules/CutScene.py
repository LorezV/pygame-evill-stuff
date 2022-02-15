from modules.Settings import *

class CutScene:
    """Реализует экран перехода на уровень. Объект класса необходимо создавать в иницилизации уровня."""
    def __init__(self, text, game):
        self.text = text
        self.printed_text = ['']
        self.current_printed_row = 0
        self.game = game
        self.duration = 5
        self.time_to_next_print = 0
        self.current_index = 0
        self.finished = False
        self.is_closed = False
        self.close_duration = 200

    def update(self):
        """Функция обновляет переменные кат-сцены."""
        if self.time_to_next_print <= 0 and not self.finished:
            sybmol = self.text[self.current_index]
            if sybmol == '\n':
                self.current_printed_row += 1
                self.printed_text.append('')
            else:
                self.printed_text[self.current_printed_row] += sybmol
            self.current_index += 1
            self.time_to_next_print += self.duration
            if len(self.text) <= self.current_index:
                self.finished = True
        else:
            self.time_to_next_print -= 1
        if self.finished and self.close_duration > 0:
            self.close_duration -= 1
        if self.close_duration <= 0:
            self.is_closed = True
            self.game.pause = False

    def render(self):
        """Функция отрисовывает элементы кат-сцены."""
        for i in range(len(self.printed_text)):
            label = self.game.bad_script.render(self.printed_text[i], 1, WHITE)
            self.game.screen.blit(label, (WIDTH // 2 - label.get_width() // 2, (HEIGHT // 2 - label.get_height() - 100) + 50 * i))
        if self.finished:
            timer = self.game.bad_script.render(str((self.close_duration // FPS) + 1), 1, WHITE)
            self.game.screen.blit(timer, (WIDTH - timer.get_width() - 100 , (HEIGHT - timer.get_height() - 100)))
        self.game.screen.blit(self.game.bad_script.render('Нажмите <Пробел> для пропуска...', 1, WHITE), (100, (HEIGHT - 100)))
        self.update()
        