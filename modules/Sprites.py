from modules.Settings import *
from collections import deque
from modules.Drawer import ray_casting_npc_player
from math import ceil
from random import sample, randint


class Sprites:
    def __init__(self, game):
        self.game = game
        self.sprite_parametrs = {
            'sprite_slender': {
                'sprite': [pygame.image.load(
                    f'data/sprites/slender/idle/1.png').convert_alpha() for i
                           in
                           range(1, 9)],
                'viewing_angles': True,
                'shift': 0,
                'scale': (1, 1),
                'side': 50,
                'animation': deque(pygame.image.load(
                    f'data/sprites/slender/animation_attack/{i}.png').convert_alpha()
                                   for i in range(11)),
                'death_animation': deque(
                    pygame.image.load(f'data/sprites/slender/animation_death/{i}.png').convert_alpha()
                    for i in range(1, 22)),
                'is_dead': False,
                'dead_shift': 0.3,
                'animation_dist': 100,
                'animation_speed': 2,
                'blocked': True,
                'is_trigger': False,
                'flag': 'npc',
                'obj_action': deque([pygame.image.load(
                    f'data/sprites/slender/animation_move/{i}.png').convert_alpha()
                                     for i in range(1, 7)])
            },
            'sprite_note': {
                'sprite': [pygame.image.load(
                    f'data/sprites/note/1.png').convert_alpha(),
                           pygame.image.load(
                               f"data/sprites/note/angled.png").convert_alpha()],
                'viewing_angles': True,
                'shift': 0,
                'scale': (0.4, 0.4),
                'side': 50,
                'animation': deque(),
                'death_animation': [],
                'is_dead': None,
                'dead_shift': None,
                'animation_dist': 50,
                'animation_speed': 8,
                'blocked': True,
                'is_trigger': True,
                'flag': 'note',
                'obj_action': deque()
            },
            'sprite_skeleton': {'sprite': [pygame.image.load(
                f'data/sprites/skeleton/idle/1.png').convert_alpha() for i
                                           in
                                           range(1, 9)],
                                'viewing_angles': True,
                                'shift': 0.2,
                                'scale': (1, 0.8),
                                'side': 50,
                                'animation': deque(pygame.image.load(
                                    f'data/sprites/skeleton/animation_attack/{i}.png').convert_alpha()
                                                   for i in range(1, 4)),
                                'death_animation': deque(
                                    pygame.image.load(f'data/sprites/skeleton/snimation_death/{i}.png').convert_alpha()
                                    for i in range(1, 4)),
                                'is_dead': False,
                                'dead_shift': 0.8,
                                'animation_dist': 70,
                                'animation_speed': 10,
                                'blocked': True,
                                'is_trigger': False,
                                'flag': 'npc',
                                'obj_action': deque([pygame.image.load(
                                    f'data/sprites/skeleton/animation_move/{i}.png').convert_alpha()
                                                     for i in range(1, 7)])

                                }
        }
        self.note_coords = sample(self.game.world.notes_spawn, 8)
        self.objects_list = []

    @property
    def sprite_shot(self):
        return min([obj.is_on_fire for obj in self.objects_list])

    def destroy_all(self):
        self.objects_list.clear()


#  def destoy_one(self, ind):
#     del self.objects_list[ind]

class SpriteObject():
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
        self.hidden = False

        self.blocked = parameters['blocked']
        self.is_trigger = parameters['is_trigger']
        self.side = parameters['side']
        self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.pos = self.x - self.side // 2, self.y - self.side // 2

        if self.viewing_angles:
            self.sprite_angles = [frozenset(range(338, 361)) | frozenset(
                range(0, 23))] + [frozenset(range(i, i + 45)) for i in
                                  range(23, 338, 45)]
            self.sprite_positions = {angle: pos for angle, pos in
                                     zip(self.sprite_angles, self.object)}

    def delta(self, x, y):
        return ((x - self.x) ** 2 + (y - self.y) ** 2) ** 0.5

    @property
    def is_on_fire(self):
        if CENTER_RAY - self.side // 2 < self.current_ray < CENTER_RAY + self.side // 2 and self.blocked:
            return self.distance, self.proj_height
        return float("inf"), None

    @property
    def sx(self):
        return self.x

    @property
    def sy(self):
        return self.y

    def object_locate(self, player):
        if not self.hidden:
            dx, dy = self.x - player.x, self.y - player.y
            self.distance = math.sqrt(dx ** 2 + dy ** 2)

            self.theta = math.atan2(dy, dx)
            gamma = self.theta - player.angle
            if dx > 0 and 180 <= math.degrees(player.ang) <= 360 or \
                    dx < 0 and dy < 0:
                gamma += DOUBLE_PI
            self.theta -= 1.4 * gamma

            delta_rays = int(gamma / DELTA_ANGLE)
            self.current_ray = CENTER_RAY + delta_rays
            self.distance *= math.cos(
                HALF_FOV - self.current_ray * DELTA_ANGLE)

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
                    sprite_object = self.sprite_animation(player)

                if player.game.pause:
                    sprite_object = self.visible_sprite()

                sprite_pos = (self.current_ray * SCALE - half_sprite_width,
                              HALF_HEIGHT - half_sprite_height + shift)
                sprite = pygame.transform.scale(
                    sprite_object, (sprite_width, sprite_height))
                return self.distance, sprite, sprite_pos
            else:
                return False,
        else:
            return False,

    def sprite_animation(self, player):
        if self.animation and self.distance < self.animation_dist:
            sprite_object = self.animation[0]
            if self.animation_count < self.animation_speed:
                self.animation_count += 1
                player.set_health(player.health - 2)
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


noteicons_group = pygame.sprite.Group()


class NoteIcon(pygame.sprite.Sprite):
    def __init__(self, image, image_unfound):
        super().__init__()
        self.founded = False
        self.icon = image
        self.icon_unfound = image_unfound

        self.image = self.icon_unfound
        self.rect = self.image.get_rect()
        noteicons_group.add(self)

    def update(self, *args, **kwargs):
        pass

    def set_founded(self):
        self.founded = True
        self.image = self.icon

    def move(self, x, y):
        self.rect.x, self.rect.y = x, y


class Note(SpriteObject):
    def __init__(self, parameters, pos, textures, title, note_icon):
        super().__init__(parameters, pos)
        self.object = textures
        self.title = title

        self.noteIcon = note_icon

        if self.viewing_angles:
            self.sprite_angles = [frozenset(range(325, 361)) | frozenset(
                range(1, 45))] + [frozenset(range(46, 325))]
            self.sprite_positions = {angle: pos for angle, pos in
                                     zip(self.sprite_angles, self.object)}


class Skeleton(SpriteObject):
    def __init__(self, parameters, pos, game):
        super().__init__(parameters, pos)
        self.game = game

        self.rect = pygame.Rect(*self.pos, 50, 50)
        self.attack_cooldown = 1 * FPS
        self.count = 0
        self.attack_sound = pygame.mixer.Sound(
            'data/sprites/skeleton/sounds/attack.mp3')
        self.sprite_angles = [frozenset(range(i, i + 1)) for i in
                              range(361)]
        self.sprite_positions = {angle: self.object[0] for angle in
                                 self.sprite_angles}
        self.death_sound = pygame.mixer.Sound('data/sprites/skeleton/sounds/skeleton_death.mp3')
        self.last_player_pos = (self.x, self.y)
        self.health = 1

    def detect_collision(self, dx, dy):
        collision_list = self.game.world.collision_objects
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)
        hit_indexes = next_rect.collidelistall(collision_list)

        if len(hit_indexes):
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

    def sprite_animation(self, player):
        if self.animation and self.distance < self.animation_dist and \
                self.attack_cooldown <= 0:
            sprite_object = self.animation[0]
            self.attack_player(player)
            return sprite_object
        return self.object

    def move(self, player, flag=False):
        if self.distance > self.animation_dist or (
                (self.x - player.pos[0]) ** 2 + (
                self.y - player.pos[1]) ** 2) ** 0.5 > self.animation_dist:
            dx = self.sx - player.pos[0]
            dy = self.sy - player.pos[1]
            dx = 1 if dx < 0 else - 1
            dy = 1 if dy < 0 else - 1
            self.detect_collision(dx, dy)
            self.rect.center = self.x, self.y
            self.pos = (self.x, self.y)
        if flag:
            x, y = self.last_player_pos
            px, py = ceil(x // TILE), ceil(y // TILE)
            sx, sy = ceil(self.x // TILE), ceil(self.y // TILE)
            visited = bfs(px, py, sx, sy, self.game.world.conj_dict)
            cur_node = (px, py)
            last = cur_node
            while cur_node != (sx, sy):
                last = cur_node
                cur_node = visited[cur_node]
            if last[0] > sx:
                dx = 1
            elif last[0] < sx:
                dx = -1
            else:
                if self.x % TILE < self.side:
                    dx = 1
                elif self.x % TILE > TILE - self.side:
                    dx = -1
                else:
                    dx = 0
            if last[1] > sy:
                dy = 1
            elif last[1] < sy:
                dy = -1
            else:
                if self.y % TILE < self.side:
                    dy = 1
                elif self.y % TILE > TILE - self.side:
                    dy = -1
                else:
                    dy = 0
            self.detect_collision(dx, dy)
            self.rect.center = self.x, self.y
            self.pos = (self.x, self.y)

    def attack_player(self, player):
        if self.animation_count < self.animation_speed:
            self.animation_count += 1
        else:
            self.animation.rotate()
            self.animation_count = 0
            self.count += 1
        if self.count == 3:
            self.attack_sound.play()
            self.attack_cooldown = 1 * FPS
            self.count = 0
            attack = randint(10, 20)
            player.set_health(player.health - attack)

    def action(self, player):
        self.attack_cooldown -= 1
        self.npc_action_trigger = False
        delta = self.delta(player.x, player.y)
        if self.attack_cooldown <= 0:
            if delta < self.animation_dist:
                self.attack_player(player)
            if ray_casting_npc_player(self.sx, self.sy, self.game.world.world_map, player.pos) or \
                    self.delta(player.x, player.y) < 70:
                self.npc_action_trigger = True
                self.last_player_pos = player.x, player.y
                self.move(player)
                return
            else:
                self.move(player, True)
            while self.count != 3:
                self.count += 1
                self.animation_count += 1
                self.animation.rotate()
            self.animation_count = 0
            self.count = 0
            self.npc_action_trigger = False

    def update(self, player):
        if not self.is_dead:
            self.action(player)


class Slender(SpriteObject):
    def __init__(self, parameters, pos, game):
        super().__init__(parameters, pos)
        self.game = game
        self.rect = pygame.Rect(*self.pos, 50, 50)
        self.slender_sound = pygame.mixer.Sound(
            'data/sprites/slender/sounds/moving.mp3')
        self.slender_sound.play(-1)
        self.attack_sound = pygame.mixer.Sound(
            'data/sprites/slender/sounds/attack.mp3')
        self.slender_sound.set_volume(0)
        self.death_sound = pygame.mixer.Sound('data/sprites/slender/sounds/death_sound.mp3')
        self.attack_cooldown = 200
        self.count = 0
        self.sprite_angles = [frozenset(range(i, i + 1)) for i in
                              range(361)]
        self.sprite_positions = {angle: self.object[0] for angle in
                                 self.sprite_angles}
        self.active_time = 0
        self.sleep = 5 * FPS
        self.health = 1

    def dead_animation(self):
        self.animation_speed = FPS
        if len(self.death_animation):
            if self.death_animation_count < self.animation_speed:
                self.dead_sprite = self.death_animation[0]
                self.death_animation_count += 1
            else:
                self.dead_sprite = self.death_animation.popleft()
                self.death_animation_count = 0
        return self.dead_sprite

    def detect_collision(self, dx, dy):
        collision_list = self.game.world.collision_objects
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)
        hit_indexes = next_rect.collidelistall(collision_list)

        if len(hit_indexes):
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

    def sprite_animation(self, player):
        if self.animation and self.distance < self.animation_dist and \
                self.attack_cooldown <= 0:
            sprite_object = self.animation[0]
            self.attack_player(player)
            return sprite_object
        return self.object

    def move(self, player):
        if self.distance > self.animation_dist or (
                (self.x - player.pos[0]) ** 2 + (
                self.y - player.pos[1]) ** 2) ** 0.5 > self.animation_dist:
            dx = self.sx - player.pos[0]
            dy = self.sy - player.pos[1]
            dx = 2 if dx < 0 else - 2
            dy = 2 if dy < 0 else - 2
            self.detect_collision(dx, dy)
            self.rect.center = self.x, self.y
            self.pos = (self.x, self.y)

    def attack_player(self, player):
        if self.animation_count < self.animation_speed:
            self.animation_count += 1
        else:
            self.animation.rotate()
            self.animation_count = 0
            self.count += 1
        if self.count == 5:
            self.attack_sound.play()
        elif self.count == 11:
            self.attack_cooldown = 200
            self.count = 0
            attack = randint(20, 40)
            if player.health - attack <= 0:
                self.slender_sound.stop()
            player.set_health(player.health - attack)

    def action(self, player):
        self.attack_cooldown -= 1
        self.npc_action_trigger = False
        delta = self.delta(player.x, player.y)
        if delta < 1000 and self.attack_cooldown <= 0 and not player.game.pause:
            self.slender_sound.set_volume(1 - delta / 1000)
            self.active_time += 1
        else:
            self.slender_sound.set_volume(0)
            self.active_time = 0
        if self.active_time > 10000:
            self.sleep -= 1
        if self.sleep < 0:
            self.sleep = 500
            self.active_time = 0
        if self.attack_cooldown <= 0 and self.active_time < 3000:
            px, py = ceil(player.x // TILE), ceil(player.y // TILE)
            sx, sy = ceil(self.x // TILE), ceil(self.y // TILE)
            if delta < self.animation_dist:
                self.attack_player(player)
            if ray_casting_npc_player(self.sx, self.sy,
                                      self.game.world.world_map,
                                      player.pos) or self.delta(player.x,
                                                                player.y) < 100:
                self.npc_action_trigger = True
                self.move(player)
                return
            while self.count != 11:
                self.count += 1
                self.animation_count += 1
                self.animation.rotate()
            self.animation_count = 0
            self.count = 0
            self.npc_action_trigger = False
            visited = bfs(px, py, sx, sy, self.game.world.conj_dict)
            cur_node = (px, py)
            last = cur_node
            while cur_node != (sx, sy):
                last = cur_node
                cur_node = visited[cur_node]
            if last[0] > sx:
                dx = 2
            elif last[0] < sx:
                dx = -2
            else:
                if self.x % TILE < self.side:
                    dx = 2
                elif self.x % TILE > TILE - self.side:
                    dx = -2
                else:
                    dx = 0
            if last[1] > sy:
                dy = 2
            elif last[1] < sy:
                dy = -2
            else:
                if self.y % TILE < self.side:
                    dy = 2
                elif self.y % TILE > TILE - self.side:
                    dy = -2
                else:
                    dy = 0
            self.detect_collision(dx, dy)
            self.rect.center = self.x, self.y
            self.pos = (self.x, self.y)

    def update(self, player):
        if not self.is_dead:
            self.action(player)


def bfs(px, py, sx, sy, conj_dict):
    queue = deque([(sx, sy)])
    visited = {queue[0]: None}
    while queue:
        cur_node = queue.popleft()
        if cur_node == (px, py):
            break
        for next_node in conj_dict[cur_node]:
            if next_node not in visited:
                queue.append(next_node)

                visited[next_node] = cur_node
    return visited
