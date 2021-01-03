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

for j, row in enumerate(text_map):
    for i, char in enumerate(row):
        if char == '#':
            world_map.add((i * TILE, j * TILE))
            mini_map.add((i * MAP_TILE, j * MAP_TILE))