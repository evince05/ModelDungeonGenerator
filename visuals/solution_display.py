import run


def create_grid(tile_locations, tile_types):

    """
    Creates a colorful 2D representation of the dungeon.
    :param tile_locations: The locations of all tiles.
    :param tile_types: The types of each tile (regular, start, end)
    :return: A 2D representation of the grid, stored in a string.
    """

    grid = [['X' for _ in range(run.GRID_SIZE)] for _ in range(run.GRID_SIZE)]
    for tile, location in tile_locations.items():
        row, col = map(int, location.split(','))
        if tile_types[tile] == 'start':
            grid[row][col] = '\033[33mS\033[0m'
        elif tile_types[tile] == 'end':
            grid[row][col] = '\033[92mE\033[0m'
        else:
            grid[row][col] = '\033[36mR\033[0m'

    return grid
