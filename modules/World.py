import pygame
from modules.Settings import *
from numba.core import types
from numba.typed import Dict
from numba import int32

with open('data/maps/first_lvl.txt', encoding='utf-8', mode='r') as f:
    matrix_map = list(f.readlines())
    matrix_map = [list(map(int, list(i.strip('\n')))) for i in matrix_map]


def find_new_nodes(x, y):
    points = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    good_points = []
    for i in range(4):
        dx, dy = points[i]
        if check_coords(dx, dy):
            if not matrix_map[dy][dx]:
                good_points.append((dx, dy))
    return good_points


def check_coords(x, y):
    return WORLD_WIDTH > x > -1 and WORLD_HEIGHT > y > -1


WORLD_WIDTH = len(matrix_map[0]) * TILE
WORLD_HEIGHT = len(matrix_map) * TILE
conj_dict = {}
world_map = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
mini_map = set()
collision_objects = []
for j, row in enumerate(matrix_map):
    for i, char in enumerate(row):
        if char:
            mini_map.add((i * MAP_TILE, j * MAP_TILE))
            collision_objects.append(
                pygame.Rect(i * TILE, j * TILE, TILE, TILE))
            if char == 1:
                world_map[(i * TILE, j * TILE)] = 1
            elif char == 2:
                world_map[(i * TILE, j * TILE)] = 2
        else:
            conj_dict[(i, j)] = find_new_nodes(i, j)

print(world_map)