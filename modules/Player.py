import pygame, math
from .Settings import *


class Player():
    def __init__(self):
        super().__init__()
        self.x, self.y = 100, 100

        # Перенести в settings
        self.player_speed = PLAYER_SPEED
        self.angle = PLAYER_ANGLE

    @property
    def pos(self):
        return self.x, self.y

    @property
    def ang(self):
        return self.angle

    def draw(self, surface):
        pygame.draw.circle(surface, (150, 150, 255), (self.x, self.y), 10)
        pygame.draw.line(surface, YELLOW, self.pos,
                         (self.x + 20 * math.cos(self.angle),
                          self.y + 20 * math.sin(self.angle)), 2)
        self.movement()

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.x += self.player_speed * cos_a
            self.y += self.player_speed * sin_a
        if keys[pygame.K_s]:
            self.x += -self.player_speed * cos_a
            self.y += -self.player_speed * sin_a
        if keys[pygame.K_a]:
            self.x += self.player_speed * sin_a
            self.y += -self.player_speed * cos_a
        if keys[pygame.K_d]:
            self.x += -self.player_speed * sin_a
            self.y += self.player_speed * cos_a
        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02
