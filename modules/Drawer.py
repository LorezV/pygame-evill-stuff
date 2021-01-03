import pygame
from modules.Settings import *
from modules.World import world_map, mini_map


class Drawer:
    def __init__(self, screen, screen_minimap):
        self.screen = screen
        self.screen_minimap = screen_minimap
        self.font = pygame.font.SysFont('arial', 36, bold=True)
        self.textures = {
            '2': pygame.image.load('data/textures/hospital.png').convert(),
            '1': pygame.image.load('data/textures/floor.png').convert(),
            't': pygame.image.load('data/textures/wood.png').convert()}

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, GREEN)
        self.screen.blit(render, FPS_POS)

    def mini_map(self, player):
        self.screen_minimap.fill("black")
        map_x, map_y = player.x // MAP_SCALE, player.y // MAP_SCALE
        pygame.draw.line(self.screen_minimap, "yellow", (map_x, map_y),
                         (map_x + 12 * math.cos(player.angle),
                          map_y + 12 * math.sin(player.angle)), 2)
        pygame.draw.circle(self.screen_minimap, "red",
                           (int(map_x), int(map_y)), 5)
        for x, y in mini_map:
            pygame.draw.rect(self.screen_minimap, "green",
                             (x, y, MAP_TILE, MAP_TILE))
        self.screen.blit(self.screen_minimap, MAP_POS)

    def mapping(self, a, b):
        return (a // TILE) * TILE, (b // TILE) * TILE

    def ray_casting(self, player, player_pos, player_angle):
        walls = []
        ox, oy = player_pos
        xm, ym = self.mapping(ox, oy)
        cur_angle = player_angle - HALF_FOV
        for ray in range(NUM_RAYS):
            sin_a = math.sin(cur_angle)
            cos_a = math.cos(cur_angle)
            sin_a = sin_a if sin_a else 0.000001
            cos_a = cos_a if cos_a else 0.000001

            x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
            for i in range(0, WIDTH, TILE):
                depth_v = (x - ox) / cos_a
                yv = oy + depth_v * sin_a
                tile_v = self.mapping(x + dx, yv)
                if tile_v in world_map:
                    texture_v = world_map[tile_v]
                    break
                x += dx * TILE

            y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
            for i in range(0, HEIGHT, TILE):
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
            proj_height = min(int(PROJ_COEFF / depth), 2 * HEIGHT)
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

    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda x: x[0], reverse=True):
            if obj[0]:
                _, objec, objec_pos = obj
                self.screen.blit(objec, objec_pos)
