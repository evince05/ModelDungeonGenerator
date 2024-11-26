import run

# Turn this to false if you just want to see the grid
DEBUG_HEADER = True

TILE_DISPLAY_CHARS = {
    "start": 'S',
    "end": 'E',
    "regular": 'R'
}


def create_grid(tile_locations, tile_types):
    """
    Creates a grid outlining each tile position on the map
    :param tile_locations:
    :param tile_types:
    :return: None
    """

    """
    Pseudocode:
    iterate through 2D positions (x, y)
    check if x, y matches a tile location
        get that tile's type and convert to display char
    else:
        print x at that spot
    """

    if DEBUG_HEADER:
        print("----------------------")
        print("Display Grid:")
        print("  S: Start room")
        print("  E: End room")
        print("  R: Regular room")
        print("  X: -- no room --")
        print("")

    print("----------------------")
    for x in range(run.GRID_SIZE):
        for y in range(run.GRID_SIZE):
            loc_str = f"{x},{y}"

            found_tile = False
            for (tile, location) in tile_locations.items():
                if location == loc_str:
                    # Found a match!
                    print(TILE_DISPLAY_CHARS[tile_types[tile]] + " ", end="")
                    found_tile = True
                    break

            if not found_tile:
                print("X ", end="")

        print("")

    print("----------------------")