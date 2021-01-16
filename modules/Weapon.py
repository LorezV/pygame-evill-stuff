import pygame
from modules.Settings import *
import os


class Weapon():
    def __init__(self, game):
        self.game = game

        self.weapon_name = "title"
        self.texture = pygame.transform.scale(
            pygame.image.load(f"data/sprites/player/weapon_shotgun/weapon.png").convert_alpha(), (WIDTH, HEIGHT))
        self.shot_animation = [pygame.transform.scale(
            pygame.image.load(f"data/sprites/player/weapon_shotgun/animation_shoot/{i}.png").convert_alpha(),
            (WIDTH, HEIGHT)) for i in range(len(os.listdir(f"data/sprites/player/weapon_shotgun/animation_shoot")))]
        self.reload_animation = [pygame.transform.scale(
            pygame.image.load(f"data/sprites/player/weapon_shotgun/animation_reload/{i}.png").convert_alpha(),
            (WIDTH, HEIGHT)) for i in range(len(os.listdir(f"data/sprites/player/weapon_shotgun/animation_reload")))]

        self.shoot_sound = pygame.mixer.Sound("data/sprites/player/weapon_shotgun/shoot.mp3")
        self.reload_sound = pygame.mixer.Sound("data/sprites/player/weapon_shotgun/reload.mp3")

        self.shot_animation_count = len(self.shot_animation)
        self.shot_animation_pos = 0

        self.reload_animation_count = len(self.reload_animation)
        self.reload_animation_pos = 0

        self.action_time = 0

        self.damage = 50
        self.max_ammo = 6
        self.ammo = self.max_ammo

        self.is_shooting = False
        self.is_reloading = False

    def render(self):
        sprite = self.texture
        if self.is_shooting and not self.game.pause:
            sprite = self.shot_animation[self.shot_animation_pos]
            self.shot_animation_pos += 1

            if self.shot_animation_pos >= self.shot_animation_count:
                self.is_shooting = False
                self.shot_animation_pos = 0

        elif self.is_reloading and not self.game.pause:
            sprite = self.reload_animation[self.reload_animation_pos]
            self.reload_animation_pos += 1

            if self.reload_animation_pos >= self.reload_animation_count:
                self.is_reloading = False
                self.reload_animation_pos = 0

        self.action_time -= 1
        self.game.screen.blit(sprite, (0, 0))

    def shoot_request(self):
        if self.is_shooting or self.is_reloading or self.ammo <= 0 or self.game.pause or self.action_time > 0:
            return False
        if self.is_shooting:
            return False
        self.shoot()

    def shoot(self):
        self.action_time = 30
        self.is_shooting = True
        self.ammo -= 1
        self.shoot_sound.play(0)

    def reload_request(self):
        if self.is_shooting or self.is_reloading or self.ammo == self.max_ammo or self.game.pause or self.action_time > 0:
            return False
        self.reload()

    def reload(self):
        self.action_time = (self.max_ammo - self.ammo) * 60
        self.reload_sound.play(self.max_ammo - self.ammo - 1)
        self.is_reloading = True
        self.ammo = self.max_ammo
