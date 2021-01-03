from modules.Settings import *
import pygame

text_map = [
    '111111111111',
    '1..2...2...1',
    '1..2.....2.1',
    '1.222222.221',
    '1..........1',
    '1222.2222221',
    '1..........1',
    '111111111111',
]

world_map = {}
mini_map = set()
collision_objects = []
for j, row in enumerate(text_map):
    for i, char in enumerate(row):
        if char != '.':
            mini_map.add((i * MAP_TILE, j * MAP_TILE))
            collision_objects.append(pygame.Rect(i * TILE, j * TILE, TILE, TILE))
            if char == '1':
                world_map[(i * TILE, j * TILE)] = '1'
            elif char == '2':
                world_map[(i * TILE, j * TILE)] = '2'
