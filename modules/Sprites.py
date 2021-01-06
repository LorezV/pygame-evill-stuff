import pygame
from modules.Settings import *


class Sprites:
    def __init__(self):
        self.sprite_types = {
            'slender': [pygame.image.load(
                f'data/sprites/slender/{i}.png').convert_alpha() for i in
                        range(1, 9)]
        }
        self.objects_list = [
            SpriteObject(self.sprite_types['slender'], False, (8.7, 4), 0, 1)]


class SpriteObject:
    def __init__(self, object, static, pos, shift, scale):
        self.object = object
        self.static = static
        self.pos = self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.shift = shift
        self.scale = scale
        if not static:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in
                                  range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle, pos in
                                     zip(self.sprite_angles, self.object)}

    def object_locate(self, player, walls):
        fake_walls0 = [walls[0] for i in range(FAKE_RAYS)]
        fake_walls1 = [walls[-1] for i in range(FAKE_RAYS)]
        fake_walls = fake_walls0 + walls + fake_walls1

        dx, dy = self.x - player.x, self.y - player.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        theta = math.atan2(dy, dx)
        gamma = theta - player.ang
        if dx > 0 and 180 <= math.degrees(player.ang) <= 360 or \
                dx < 0 and dy < 0:
            gamma += DOUBLE_PI

        delta_rays = int(gamma / DELTA_ANGLE)
        current_ray = CENTER_RAY + delta_rays
        distance *= math.cos(HALF_FOV - current_ray * DELTA_ANGLE)

        fake_ray = current_ray + FAKE_RAYS
        if 0 <= fake_ray <= NUM_RAYS - 1 + 2 * FAKE_RAYS and \
                distance < fake_walls[fake_ray][0]:
            proj_height = int(PROJ_COEFF / distance * self.scale)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift

            if not self.static:
                if theta < 0:
                    theta += DOUBLE_PI
                theta = 360 - int(math.degrees(theta))

                for angles in self.sprite_angles:
                    if theta in angles:
                        self.object = self.sprite_positions[angles]
                        break

            sprite_pos = (current_ray * SCALE - half_proj_height,
                          HALF_HEIGHT - half_proj_height + shift)
            sprite = pygame.transform.scale(self.object,
                                            (proj_height, proj_height))
            return distance, sprite, sprite_pos
        else:
            return False,
