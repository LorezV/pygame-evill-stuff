import pygame
from modules.Settings import *
from modules.Drawer import ray_casting_npc_player
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

        self.sfx = [pygame.image.load(f'data/sprites/player/boom/{i}.png').convert_alpha() for i in range(9)]
        self.sfx_animation_pos = 0
        self.sfx_animation_count = len(self.sfx)

        self.shot_animation_count = len(self.shot_animation)
        self.shot_animation_pos = 0

        self.reload_animation_count = len(self.reload_animation)
        self.reload_animation_pos = 0

        self.action_time = 0

        self.damage = 50
        self.max_ammo = 12
        self.ammo = self.max_ammo

        self.is_shooting = False
        self.is_reloading = False
        self.is_sfx_render = False

    def render(self, shots):
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
        if self.sfx_animation_pos < self.sfx_animation_count and self.is_sfx_render:
            self.shot_projection = min(shots)[1] // 2
            self.render_sfx()
        else:
            self.sfx_animation_pos = 0
            self.is_sfx_render = False
        self.action_time -= 1
        self.game.screen.blit(sprite, (0, 0))

    def render_sfx(self):
        sfx = pygame.transform.scale(self.sfx[self.sfx_animation_pos], (self.shot_projection, self.shot_projection))
        sfx_rect = sfx.get_rect()
        self.game.screen.blit(sfx, (HALF_WIDTH - sfx_rect.w // 2, HALF_HEIGHT - sfx_rect.h // 2))
        self.sfx_animation_pos += 1

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
        self.is_sfx_render = True
        for obj in sorted(self.game.sprites.objects_list, key=lambda obj: obj.distance):
            if obj.is_on_fire[1]:
                if obj.is_dead != "immortal" and not obj.is_dead:
                    if ray_casting_npc_player(obj.x, obj.y, self.game.world.world_map, self.game.player.pos):
                        if obj.flag == 'npc':
                            if obj.health:
                                obj.health -= 1
                            else:
                                obj.death_sound.play()
                                obj.is_dead = True
                                obj.blocked = False
                break

    def reload_request(self):
        if self.is_shooting or self.is_reloading or self.ammo == self.max_ammo or self.game.pause or self.action_time > 0:
            return False
        self.reload()

    def reload(self):
        self.action_time = 1 * 60
        self.reload_sound.play(0)
        self.is_reloading = True
        self.ammo += 1
