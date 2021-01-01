import pygame


class Player():
    def __init__(self):
        super().__init__()
        self.x, self.y = 100, 100

    def draw(self, surface):
        pygame.draw.circle(surface, (150, 150, 255), (self.x, self.y), 10)
        self.movement()

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.x += 10
        elif keys[pygame.K_LEFT]:
            self.x -= 10
        if keys[pygame.K_UP]:
            self.y -= 10
        if keys[pygame.K_DOWN]:
            self.y += 10
