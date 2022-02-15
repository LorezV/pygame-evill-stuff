from modules.Settings import *
from modules.Weapon import Weapon


class Player:
    """Класс, реализующий функционал игрока."""
    def __init__(self, game):
        super().__init__()
        self.x, self.y = PLAYER_SPAWN_POS
        self.game = game

        # Показатели игрока
        self.health = 100
        self.stamina = 100
        self.player_speed = PLAYER_SPEED
        self.angle = PLAYER_ANGLE

        self.can_run = True
        self.notes = [
            x for x in self.game.sprites.objects_list if x.flag == "note"]
        self.current_notes = []
        self.notes_sprite_group = pygame.sprite.Group()

        self.weapon = Weapon(self.game)

        # collision
        self.side = 40
        self.rect = pygame.Rect(*self.pos, self.side, self.side)

    @property
    def pos(self):
        """Вовзаращет позицию игрока в данный момент времени."""
        return self.x, self.y

    @property
    def ang(self):
        """Возвращет направление взгляда игрока."""
        return self.angle

    def detect_collision(self, dx, dy):
        """Проверка коллизии спрайтов и стен."""
        collision_sprites = [(pygame.Rect(*obj.pos, obj.side, obj.side), obj)
                             for obj in self.game.sprites.objects_list
                             if obj.blocked]
        collision_list = self.game.world.collision_objects + [x[0] for x in
                                                              collision_sprites
                                                              if not x[
                1].is_trigger]
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
        """Проверка подбора каких-либо предметов."""
        for rect, sprite in hit_sprites:
            if self.rect.colliderect(rect):
                if sprite.hidden:
                    continue
                if sprite.flag == "note":
                    sprite.noteIcon.set_founded()
                    sprite.hidden = True
                    sprite.capture_sound.play()
                    all_notes_founded = True
                    for _sprite in self.game.sprites.objects_list:
                        if _sprite.flag == "note":
                            all_notes_founded *= _sprite.hidden

                    if all_notes_founded:
                        self.game.drawer.textures[3] = \
                        self.game.drawer.door_images[1]
                        self.game.portal_open = True
                if sprite.flag == "aid":
                    self.set_health(self.health + 20)
                    sprite.hidden = True
                sprite.capture_sound.play()

    def set_health(self, health):
        """Установка здоровья игрока."""
        if health > 100:
            health = 100
        elif health < 0:
            health = 0
        self.health = health
        if self.health <= 0:
            self.game.set_level(self.game.loose)

    def set_stamina(self, stamina):
        """Установка стамины игрока."""
        if stamina > 100:
            stamina = 100
        elif stamina < 0:
            stamina = 0

        self.stamina = stamina
        if self.stamina <= 0:
            self.can_run = False
        elif self.stamina > 60:
            self.can_run = True

    def movement(self):
        """Общее движение игрока."""
        self.mouse_control()
        self.keys_control()
        self.rect.center = self.x, self.y
        self.angle %= DOUBLE_PI

        if PORTAL_COORDS[0] - 50 < self.x < PORTAL_COORDS[0] + 50 and \
                PORTAL_COORDS[1] - 50 < self.y < PORTAL_COORDS[
            1] + 50 and self.game.portal_open:
            self.game.portal_open = False
            self.game.set_level(self.game.planet_level)
            self.game.pause = False
            pygame.event.clear()

    def keys_control(self):
        """Проверка нажатых клавиш."""
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

        if keys[pygame.K_LSHIFT] and self.can_run:
            self.player_speed = PLAYER_SPEED_FAST
            self.set_stamina(self.stamina - 1)
        else:
            self.player_speed = PLAYER_SPEED
            self.set_stamina(self.stamina + 0.5)
        if keys[pygame.K_TAB]:
            self.game.render_tips = True
        else:
            self.game.render_tips = False

    def mouse_control(self):
        """Проверка изменения положения мыши"""
        if pygame.mouse.get_focused():
            difference = pygame.mouse.get_pos()[0] - HALF_WIDTH
            pygame.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))
            self.angle += difference * SENSITIVITY
