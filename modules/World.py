from modules.Settings import *
from numba.core import types
from numba.typed import Dict
from numba import int32


def find_new_nodes(x, y, matrix_map, width, height):
    points = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    good_points = []
    for i in range(4):
        dx, dy = points[i]
        if check_coords(dx, dy, width, height):
            if not matrix_map[dy][dx]:
                good_points.append((dx, dy))
    return good_points


def check_coords(x, y, width, height):
    return width > x > -1 and height > y > -1


def load_map(path):
    with open(path, encoding='utf-8', mode='r') as f:
        level = list(f.readlines())
        level = [list(map(int, list(i.strip('\n')))) for i in level]
    width = len(level[0]) * TILE
    height = len(level) * TILE
    conj_dict = {}
    world_map = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
    mini_map = set()
    collision_objects = []
    # notes_spawn = [(2, 2), (2, 2.2), (2, 2.4), (2, 2.6), (2, 2.8), (2, 3), (2, 3.2), (2, 3.4)]
    notes_spawn = []
    for j, row in enumerate(level):
        for i, char in enumerate(row):
            if char:
                mini_map.add((i * MAP_TILE, j * MAP_TILE))
                collision_objects.append(
                    pygame.Rect(i * TILE, j * TILE, TILE, TILE))
                world_map[(i * TILE, j * TILE)] = char
            else:
                conj_dict[(i, j)] = find_new_nodes(i, j, level, width, height)
                if i != len(level[0]) - 1 and level[j][i + 1] == 2:
                    notes_spawn.append((i, j))
    return conj_dict, world_map, collision_objects, mini_map, notes_spawn, width, height


conj_dict, world_map, collision_objects, mini_map, notes_spawn, WORLD_WIDTH, WORLD_HEIGHT = load_map(
    'data/maps/first_lvl.txt')
