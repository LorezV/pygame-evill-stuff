from modules.Settings import *


class Button(pygame.rect.Rect):
    def __init__(self, text, event, game):
        self.text = text
        self.game = game
        self.size = (400, 100)
        self.color = WHITE
        self.background_color = BLACK
        self.event_to_post = event
        super().__init__(((0, 0) + self.size))

    def draw(self):
        button_text = self.game.font.render(self.text, 1, self.color)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if self.collidepoint(mouse_pos):
            pygame.draw.rect(self.game.screen, self.background_color, self, border_radius=25)
            if mouse_click[0]:
                pygame.event.post(self.event_to_post)

        self.game.screen.blit(button_text, (
            self.centerx - button_text.get_width() // 2, self.centery - button_text.get_height() // 2))
        pygame.draw.rect(self.game.screen, self.color, self, width=10, border_radius=25)

    def move_bc(self, x, y):
        self.centerx, self.centery = x, y
