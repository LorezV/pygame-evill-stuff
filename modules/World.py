from modules.Settings import *
from numba.core import types
from numba.typed import Dict
from numba import int32


class World:
    def __init__(self, path):
        self.path = path
        self.conj_dict, self.world_map, self.collision_objects, self.mini_map, self.notes_spawn, self.WORLD_WIDTH, self.WORLD_HEIGHT = self.load_map(
            self.path)

    def load_map(self, path):
        with open(path, encoding='utf-8', mode='r') as f:
            level = list(f.readlines())
            level = [list(map(int, list(i.strip('\n')))) for i in level]
        width = len(level[0]) * TILE
        height = len(level) * TILE
        conj_dict = {}
        world_map = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
        mini_map = set()
        collision_objects = []
        notes_spawn = []
        notes_spawn = [(2, 2), (2, 2.2), (2, 2.4), (2, 2.6), (2, 2.8), (2, 3), (2, 3.2), (2, 3.4)]
        for j, row in enumerate(level):
            for i, char in enumerate(row):
                if char:
                    mini_map.add((i * MAP_TILE, j * MAP_TILE))
                    collision_objects.append(
                        pygame.Rect(i * TILE, j * TILE, TILE, TILE))
                    world_map[(i * TILE, j * TILE)] = char
                else:
                    conj_dict[(i, j)] = self.find_new_nodes(i, j, level, width, height)
                    if i != len(level[0]) - 1 and level[j][i + 1] == 2:
                        # notes_spawn.append((i, j))
                        pass
        return conj_dict, world_map, collision_objects, mini_map, notes_spawn, width, height

    def check_coords(self, x, y, width, height):
        return width > x > -1 and height > y > -1

    def find_new_nodes(self, x, y, matrix_map, width, height):
        points = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        good_points = []
        for i in range(4):
            dx, dy = points[i]
            if self.check_coords(dx, dy, width, height):
                if not matrix_map[dy][dx]:
                    good_points.append((dx, dy))
        return good_points
