import pygame
from modules.Settings import *
from modules.World import collision_objects


class Player:
    def __init__(self, sprites):
        super().__init__()
        self.x, self.y = 150, 150
        self.sensitivity = SENSITIVITY

        self.sprites = sprites

        # Перенести в settings
        self.player_speed = PLAYER_SPEED
        self.angle = PLAYER_ANGLE

        self.health = 100
        self.stamina = 100
        self.can_run = True

        # collision
        self.side = 40
        self.rect = pygame.Rect(*self.pos, self.side, self.side)
        # self.collision_sprites = [pygame.Rect(*obj.pos, obj.side, obj.side) for
        #                           obj in self.sprites.objects_list if
        #                           obj.blocked]
        # self.collision_list = collision_objects + self.collision_sprites

    @property
    def pos(self):
        return self.x, self.y

    @property
    def ang(self):
        return self.angle

    def detect_collision(self, dx, dy):
        collision_sprites = [(pygame.Rect(*obj.pos, obj.side, obj.side), obj) for obj in self.sprites.objects_list
                             if obj.blocked]
        collision_list = collision_objects + [x[0] for x in collision_sprites if not x[1].is_trigger]
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)
        hit_indexes = next_rect.collidelistall(collision_list)

        if len(hit_indexes):
            self.on_player_collision_entered(collision_sprites)
            delta_x, delta_y = 0, 0
            for hit_index in hit_indexes:
                hit_rect = collision_list[hit_index]
                if dx > 0:
                    delta_x += next_rect.right - hit_rect.left
                else:
                    delta_x += hit_rect.right - next_rect.left
                if dy > 0:
                    delta_y += next_rect.bottom - hit_rect.top
                else:
                    delta_y += hit_rect.bottom - next_rect.top

            if abs(delta_x - delta_y) < 10:
                dx, dy = 0, 0
            elif delta_x > delta_y:
                dy = 0
            elif delta_y > delta_x:
                dx = 0
        self.x += dx
        self.y += dy

    def on_player_collision_entered(self, hit_sprites):
        for rect, sprite in hit_sprites:
            if sprite.flag == "note" and self.rect.colliderect(rect):
                del self.sprites.objects_list[self.sprites.objects_list.index(sprite)]

    def check_value(self, value):
        value = int(value)
        if value > 100:
            value = 100
        elif value < 0:
            value = 0

        return value

    def set_health(self, health):
        self.health = self.check_value(health)

    def set_stamina(self, stamina):
        self.stamina = self.check_value(stamina)
        if self.stamina == 0:
            self.can_run = False
        elif self.stamina > 50:
            self.can_run = True

    def movement(self):
        self.mouse_control()
        self.keys_control()
        self.rect.center = self.x, self.y
        self.angle %= DOUBLE_PI

    def keys_control(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            dx = self.player_speed * cos_a
            dy = self.player_speed * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_s]:
            dx = -self.player_speed * cos_a
            dy = -self.player_speed * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_a]:
            dx = self.player_speed * sin_a
            dy = -self.player_speed * cos_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_d]:
            dx = -self.player_speed * sin_a
            dy = self.player_speed * cos_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02

        if keys[pygame.K_SPACE]:
            self.set_health(25)

        if keys[pygame.K_LSHIFT] and self.can_run:
            self.player_speed = PLAYER_SPEED + 1
            self.set_stamina(self.stamina - 2)
        else:
            self.player_speed = PLAYER_SPEED
            self.set_stamina(self.stamina + 1)

    def mouse_control(self):
        if pygame.mouse.get_focused():
            difference = pygame.mouse.get_pos()[0] - HALF_WIDTH
            pygame.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))
            self.angle += difference * self.sensitivity
