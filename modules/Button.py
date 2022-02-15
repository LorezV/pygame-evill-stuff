from modules.Settings import *

class Button(pygame.rect.Rect):
    """Класс описывает кнопку, реализует эффект при наведении, масштабирование размера прямоугольника под текст кнопки."""
    def __init__(self, text, event, game):
        self.text = text
        self.game = game
        self.color = WHITE
        self.background_color = BLACK
        self.event_to_post = event
        self.button_text = self.game.font.render(self.text, 1, self.color)
        self.size = (self.button_text.get_width() + 40, 100)
        super().__init__(((0, 0) + self.size))

    def draw(self):
        """Отрисовка кнопки, отслеживание наведения мыши и её нажатия на кнопку."""
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        self.button_text = self.game.font.render(self.text, 1, self.color)

        if self.collidepoint(mouse_pos):
            pygame.draw.rect(self.game.screen, self.background_color, self, border_radius=25)
            if mouse_click[0]:
                pygame.event.post(self.event_to_post)

        self.game.screen.blit(self.button_text, (self.centerx - self.button_text.get_width() // 2, self.centery - self.button_text.get_height() // 2))
        pygame.draw.rect(self.game.screen, self.color, self, width=10, border_radius=25)
        
    def move_bc(self, x, y):
        """Перемещение кнопки, относительно ее центра."""
        self.centerx, self.centery = x, y
