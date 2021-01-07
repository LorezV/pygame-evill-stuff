from modules.Settings import *
import pygame
from numba.core import types
from numba.typed import Dict
from numba import int32

with open('data/maps/first_lvl.txt', encoding='utf-8', mode='r') as f:
    matrix_map = list(f.readlines())
    matrix_map = [list(map(int, list(i.strip('\n')))) for i in matrix_map]

WORLD_WIDTH = len(matrix_map[0]) * TILE
WORLD_HEIGHT = len(matrix_map) * TILE
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
