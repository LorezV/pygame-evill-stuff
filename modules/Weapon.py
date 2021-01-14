import pygame
from modules.Settings import *


class Weapon:
    def __init__(self, weapon_name, texture_path):
        self.weapon_name = weapon_name
        self.texture = pygame.transform.scale(pygame.image.load(texture_path).convert_alpha(), (WIDTH, HEIGHT))
        self.max_ammo = 30
        self.ammo = self.max_ammo

    def shoot_request(self):
        if self.ammo <= 0:
            return self.reload()
        self.shoot()

    def shoot(self):
        self.ammo -= 1

    def reload(self):
        self.ammo = self.max_ammo
