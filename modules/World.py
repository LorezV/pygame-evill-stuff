from modules.Settings import *

text_map = [
    '############',
    '#..#...#...#',
    '#..#.....#.#',
    '#.######.###',
    '#..........#',
    '####.#######',
    '#..........#',
    '############'
]

world_map = set()
for j, row in enumerate(text_map):
    for i, char in enumerate(row):
        if char == '#':
            world_map.add((i * TILE, j * TILE))
