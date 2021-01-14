import os
from modules.Settings import *

class SpriteEntity():
    def __init__(self, textures_folder, pos):
        self.textures = {
            filename.split('.')[0]: pygame.image.load(f"data/sprites/{textures_folder}/idle/{filename}").convert_alpha() for
            filename in os.listdir(f"data/sprites/{textures_folder}/idle/")}
        self.has_viewing_angles = False
        self.shift = 0
        self.scale = (1, 1)
        self.side = 30
        self.blocked = True

        self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.pos = self.x - self.side // 2, self.y - self.side // 2

        if self.has_viewing_angles:
            self.sprite_viewing_angles = [
                frozenset(range(338, 361)) | frozenset(range(i, i + 45) for i in range(23, 338, 45))]
            self.sprite_positions = {angle: pos for angle, pos in
                                     zip(self.sprite_viewing_angles, self.textures.values())}

    @property
    def sx(self):
        return self.x

    @property
    def xy(self):
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

            self.textures = self.visible_sprite()

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

    def visible_sprite(self):
        if self.viewing_angles:
            if self.theta < 0:
                self.theta += DOUBLE_PI
            self.theta = 360 - int(math.degrees(self.theta))

            for angles in self.sprite_angles:
                if self.theta in angles:
                    return self.sprite_positions[angles]
        return self.textures
