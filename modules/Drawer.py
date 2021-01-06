import pygame
from modules.Settings import *
from modules.World import world_map, mini_map, WORLD_WIDTH, WORLD_HEIGHT


class Drawer:
    def __init__(self, screen, screen_minimap):
        self.screen = screen
        self.screen_minimap = screen_minimap
        self.font = pygame.font.SysFont('arial', 26, bold=True)
        self.textures = {
            2: pygame.image.load('data/textures/hospital.png').convert(),
            1: pygame.image.load('data/textures/floor.png').convert(),
            't': pygame.image.load('data/textures/wood.png').convert()}

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, GREEN)
        self.screen.blit(render, FPS_POS)

    def mini_map(self, player):
        self.screen_minimap.fill("black")
        map_x, map_y = player.x // MAP_SCALE, player.y // MAP_SCALE
        map_x_col, map_y_col = player.rect.x // MAP_SCALE, player.rect.y // MAP_SCALE
        pygame.draw.line(self.screen_minimap, YELLOW, (map_x, map_y),
                         (map_x + 12 * math.cos(player.angle),
                          map_y + 12 * math.sin(player.angle)), 2)

        # Draw collision rect
        # pygame.draw.rect(self.screen_minimap, "green", (
        # player.rect.x // MAP_SCALE, player.rect.y // MAP_SCALE, player.rect.width // MAP_SCALE,
        # player.rect.height // MAP_SCALE))

        pygame.draw.circle(self.screen_minimap, RED,
                           (int(map_x), int(map_y)), 5)
        for x, y in mini_map:
            pygame.draw.rect(self.screen_minimap, GREEN,
                             (x, y, MAP_TILE, MAP_TILE))
        self.screen.blit(self.screen_minimap, MAP_POS)

    def mapping(self, a, b):
        return (a // TILE) * TILE, (b // TILE) * TILE

    def ray_casting(self, player, player_pos, player_angle):
        walls = []
        ox, oy = player_pos
        texture_v, texture_h = 1, 1
        xm, ym = self.mapping(ox, oy)
        cur_angle = player_angle - HALF_FOV
        for ray in range(NUM_RAYS):
            sin_a = math.sin(cur_angle)
            cos_a = math.cos(cur_angle)
            sin_a = sin_a if sin_a else 0.000001
            cos_a = cos_a if cos_a else 0.000001

            x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
            for i in range(0, WORLD_WIDTH, TILE):
                depth_v = (x - ox) / cos_a
                yv = oy + depth_v * sin_a
                tile_v = self.mapping(x + dx, yv)
                if tile_v in world_map:
                    texture_v = world_map[tile_v]
                    break
                x += dx * TILE

            y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
            for i in range(0, WORLD_HEIGHT, TILE):
                depth_h = (y - oy) / sin_a
                xh = ox + depth_h * cos_a
                tile_h = self.mapping(xh, y + dy)
                if tile_h in world_map:
                    texture_h = world_map[tile_h]
                    break
                y += dy * TILE

            depth, offset, texture = (
                depth_v, yv, texture_v) if depth_v < depth_h else (
                depth_h, xh, texture_h)
            offset = int(offset) % TILE
            depth *= math.cos(player.ang - cur_angle)
            depth = max(depth, 0.0000001)
            proj_height = min(int(PROJ_COEFF / depth), PENTA_HEIGHT)
            wall_column = self.textures[texture].subsurface(
                offset * TEXTURE_SCALE, 0,
                TEXTURE_SCALE,
                TEXTURE_HEIGHT)
            wall_column = pygame.transform.scale(wall_column,
                                                 (SCALE, proj_height))
            walls_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            walls.append((depth, wall_column, walls_pos))
            cur_angle += DELTA_ANGLE
        return walls

    def background(self, angle):
        top_offset = -5 * math.degrees(angle) % WIDTH
        self.screen.blit(self.textures['t'], (top_offset, 0))
        self.screen.blit(self.textures['t'], (top_offset - WIDTH, 0))
        self.screen.blit(self.textures['t'], (top_offset + WIDTH, 0))

        pygame.draw.rect(self.screen, BLACK,
                         (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))
        pass

    def interface(self, player):
        # Player health
        pygame.draw.rect(self.screen, BLACK, (MARGIN, MARGIN, HEALTH_WIDTH, HEALTH_HEIGHT))
        pygame.draw.rect(self.screen, RED, (
            MARGIN + PADDING, MARGIN + PADDING, HEALTH_WIDTH * player.health // 100 - PADDING * 2,
            HEALTH_HEIGHT - PADDING * 2))
        health_text = self.font.render(str(player.health) + "%", 1, WHITE)
        self.screen.blit(health_text, (HEALTH_TEXT_POS_X - health_text.get_width() // 2,
                                       HEALTH_TEXT_POS_Y - health_text.get_height() // 2))

        # Player stamina
        pygame.draw.rect(self.screen, BLACK, (STAMINA_POS_X, STAMINA_POS_Y, STAMINA_WIDTH, STAMINA_HEIGHT))
        pygame.draw.rect(self.screen, BLUE, (
            STAMINA_POS_X + PADDING, STAMINA_POS_Y + PADDING, STAMINA_WIDTH * player.stamina // 100 - PADDING * 2,
            STAMINA_HEIGHT - PADDING * 2))
        stamina_text = self.font.render(str(player.stamina) + "%", 1, WHITE)
        self.screen.blit(stamina_text, (STAMINA_TEXT_POS_X - stamina_text.get_width() // 2,
                                       STAMINA_TEXT_POS_Y - stamina_text.get_height() // 2))

    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda x: x[0], reverse=True):
            if obj[0]:
                _, objec, objec_pos = obj
                self.screen.blit(objec, objec_pos)
