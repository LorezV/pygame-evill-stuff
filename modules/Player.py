import pygame
from modules.Settings import *


class Player():
    def __init__(self):
        super().__init__()
        self.x, self.y = 200, 200
        self.sensitivity = SENSITIVITY

        # Перенести в settings
        self.player_speed = PLAYER_SPEED
        self.angle = PLAYER_ANGLE

    @property
    def pos(self):
        return self.x, self.y

    @property
    def ang(self):
        return self.angle

    def movement(self):
        self.keys_control()
        self.mouse_control()
        self.angle %= DOUBLE_PI

    def keys_control(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            exit()
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

    def mouse_control(self):
        if pygame.mouse.get_focused():
            difference = pygame.mouse.get_pos()[0] - HALF_WIDTH
            pygame.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))
            self.angle += difference * self.sensitivity
