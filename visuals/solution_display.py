import run

# Turn this to false if you just want to see the grid
DEBUG_HEADER = True

def create_grid(tile_locations, tile_types):

    if DEBUG_HEADER:
        print("----------------------")
        print("Display Grid:")
        print("  S: Start room")
        print("  E: End room")
        print("  R: Regular room")
        print("  X: -- no room --")
        print("")

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
