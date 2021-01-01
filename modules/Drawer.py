import pygame
from modules.Settings import *
from modules.World import world_map


class Drawer:
    def __init__(self, screen):
        self.scr = screen

    def ray_casting(self, player_pos, player_angle):
        cur_angle = player_angle - HALF_FOV
        xo, yo = player_pos
        for ray in range(NUM_RAYS):
            sin_a = math.sin(cur_angle)
            cos_a = math.cos(cur_angle)
            for depth in range(MAX_DEPTH):
                x = xo + depth * cos_a
                y = yo + depth * sin_a
                if (x // TILE * TILE, y // TILE * TILE) in world_map:
                    depth *= math.cos(player_angle - cur_angle)
                    proj_height = min(PROJ_COEFF / (depth + 0.0001), HEIGHT)
                    c = 255 / (1 + depth * depth * 0.0001)
                    color = (c // 2, c, c // 3)
                    pygame.draw.rect(self.scr, color, (
                        ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE,
                        proj_height))
                    break
            cur_angle += DELTA_ANGLE
