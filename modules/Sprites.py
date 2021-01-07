import pygame
from modules.Settings import *
from collections import deque


class Sprites:
    def __init__(self):
        self.sprite_parametrs = {
            'sprite_slender': {
                'sprite': [pygame.image.load(
                    f'data/sprites/slender/{i}.png').convert_alpha() for i in
                           range(1, 9)],
                'viewing_angles': True,
                'shift': 0,
                'scale': (1, 1),
                'side': 30,
                'animation': deque(pygame.image.load(
                    f'data/sprites/slender_animation/attack{i}.png').convert_alpha()
                                   for i in range(11)),
                'death_animation': [],
                'is_dead': None,
                'dead_shift': None,
                'animation_dist': 200,
                'animation_speed': 8,
                'blocked': True,
                'flag': 'npc',
                'obj_action': deque([pygame.image.load(
                    f'data/sprites/slender_move/move{i}.png').convert_alpha()
                                     for i in range(1, 3)])
            },
        }
        self.objects_list = [
            SpriteObject(self.sprite_parametrs['sprite_slender'], (8.7, 4))]


class SpriteObject:
    def __init__(self, parameters, pos):
        self.object = parameters['sprite'].copy()
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation'].copy()

        self.death_animation = parameters['death_animation'].copy()
        self.is_dead = parameters['is_dead']
        self.dead_shift = parameters['dead_shift']

        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.animation_count = 0

        self.flag = parameters['flag']
        self.obj_action = parameters['obj_action'].copy()
        self.death_animation_count = 0
        self.npc_action_trigger = False

        self.blocked = parameters['blocked']
        self.side = parameters['side']
        self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.pos = self.x - self.side // 2, self.y - self.side // 2

        if self.viewing_angles:
            self.sprite_angles = [frozenset(range(338, 361)) | frozenset(
                range(0, 23))] + [frozenset(range(i, i + 45)) for i in
                                  range(23, 338, 45)]
            self.sprite_positions = {angle: pos for angle, pos in
                                     zip(self.sprite_angles, self.object)}

    @property
    def sx(self):
        return self.x

    @property
    def sy(self):
        return self.y

    def object_locate(self, player):
        dx, dy = self.x - player.x, self.y - player.y
        self.distance = math.sqrt(dx ** 2 + dy ** 2)

        self.theta = math.atan2(dy, dx)
        gamma = self.theta - player.ang
        if dx > 0 and 180 <= math.degrees(player.ang) <= 360 or \
                dx < 0 and dy < 0:
            gamma += DOUBLE_PI
        self.theta -= 1.4 * gamma

        delta_rays = int(gamma / DELTA_ANGLE)
        self.current_ray = CENTER_RAY + delta_rays
        self.distance *= math.cos(HALF_FOV - self.current_ray * DELTA_ANGLE)

        fake_ray = self.current_ray + FAKE_RAYS
        if 0 <= fake_ray <= FAKE_RAYS_RANGE and self.distance > 30:
            self.proj_height = min(int(PROJ_COEFF / self.distance),
                                   DOUBLE_HEIGHT)
            sprite_width = int(self.proj_height * self.scale[0])
            sprite_height = int(self.proj_height * self.scale[1])
            half_sprite_width = sprite_width // 2
            half_sprite_height = sprite_height // 2
            shift = half_sprite_height * self.shift

            if self.is_dead and self.is_dead != 'immortal':
                sprite_object = self.dead_animation()
                shift = half_sprite_height * self.dead_shift
                sprite_height = int(sprite_height / 1.3)
            elif self.npc_action_trigger and self.distance >= self.animation_dist:
                sprite_object = self.npc_in_action()
            else:
                self.object = self.visible_sprite()
                sprite_object = self.sprite_animation()

            sprite_pos = (self.current_ray * SCALE - half_sprite_width,
                          HALF_HEIGHT - half_sprite_height + shift)
            sprite = pygame.transform.scale(
                sprite_object, (sprite_width, sprite_height))
            return self.distance, sprite, sprite_pos
        else:
            return False,

    def sprite_animation(self):
        if self.animation and self.distance < self.animation_dist:
            sprite_object = self.animation[0]
            if self.animation_count < self.animation_speed:
                self.animation_count += 1
            else:
                self.animation.rotate()
                self.animation_count = 0
            return sprite_object
        return self.object

    def visible_sprite(self):
        if self.viewing_angles:
            if self.theta < 0:
                self.theta += DOUBLE_PI
            self.theta = 360 - int(math.degrees(self.theta))

            for angles in self.sprite_angles:
                if self.theta in angles:
                    return self.sprite_positions[angles]
        return self.object

    def dead_animation(self):
        if len(self.death_animation):
            if self.death_animation_count < self.animation_speed:
                self.dead_sprite = self.death_animation[0]
                self.death_animation_count += 1
            else:
                self.dead_sprite = self.death_animation.popleft()
                self.death_animation_count = 0
        return self.dead_sprite

    def npc_in_action(self):
        sprite_object = self.obj_action[0]
        if self.animation_count < self.animation_speed:
            self.animation_count += 1
        else:
            self.obj_action.rotate()
            self.animation_count = 0
        return sprite_object
