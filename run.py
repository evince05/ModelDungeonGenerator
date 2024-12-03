from bauhaus import Encoding, proposition, constraint, And
from nnf import config

import visuals.solution_display as display

# Use a faster SAT solver
config.sat_backend = "kissat"

# Encoding for the full-sized test
E = Encoding()

# Constants for the full problem size
NUM_TILES = 7  # 1 start, 1 end, 5 regular
GRID_SIZE = 2 * NUM_TILES - 1  # 13x13 grid grid

TILES = [f"t{i}" for i in range(NUM_TILES)]
SPECIAL_TILES = ["start", "end"]

REGULAR_TILES = TILES[2:]  # Exclude start and end
LOCATIONS = [f"{row},{col}" for row in range(GRID_SIZE) for col in range(GRID_SIZE)]

# For handling connections. DIRECTION_OPPOSITES should make it easier to calculate the implications
DIRECTIONS = ['N', 'E', 'S', 'W']
DIRECTION_OPPOSITES = {
    'N': 'S',
    'E': 'W',
    'S': 'N',
    'W': 'E'
}


@proposition(E)
class RoomType:
    def __init__(self, tile, room_type):
        assert tile in TILES
        assert room_type in SPECIAL_TILES + ["regular"]
        self.tile = tile
        self.room_type = room_type

    def _prop_name(self):
        return f"RoomType({self.tile}={self.room_type})"


@proposition(E)
class OccupiedLocation:
    def __init__(self, tile, location):
        assert tile in TILES
        assert location in LOCATIONS
        self.tile = tile
        self.location = location

        loc = location.split(",")
        assert len(loc) == 2

        self.x = int(loc[0])
        self.y = int(loc[1])

    def _prop_name(self):
        return f"Location({self.tile}@{self.location})"

    def x(self):
        """
        Returns the x-value of the location
        :return:
        """
        return self.x

    def y(self):
        """
        Returns the y-value of the location
        :return:
        """
        return self.y

@proposition(E)
class Connected:
    def __init__(self, tile_i, tile_j: OccupiedLocation, direction):

        assert tile_i != tile_j
        assert tile_i in TILES and tile_j in TILES

        assert direction in DIRECTIONS

        """
        It seems like propositions are just initializing the values. Comment this out for now. 
        """
        # if direction == 'N':
        #     assert loc_i.x == loc_j.x and loc_j.y - loc_i.y == 1
        # elif direction == 'S':
        #     assert loc_i.x == loc_j.x and loc_j.y - loc_i.y == -1
        # elif direction == 'E':
        #     assert loc_j.x - loc_i.x == 1 and loc_i.y == loc_j.y
        # else:  # direction == W
        #     assert loc_j.x - loc_i.x == -1 and loc_i.y == loc_j.y

        self.tile_i = tile_i
        self.tile_j = tile_j
        self.direction = direction

    def _prop_name(self):
        return f"Connected ({self.tile_i}), ({self.tile_j}) [{self.direction}]"


def apply_constraints():
    # Ensure exactly one start and one end tile

    """
    NOTE: Be careful when adding constraints!
    constraint.add_exactly_one(E, list_constraints) makes sure that only one constraint from list_constraints is true
    so, constraint.add_exactly_one(E, [RoomType(tile, "regular") for tile in REGULAR_TILES]) makes only ONE tile regular.
    """

    # Forced tiles [0] and [1] to be start/end tiles (avoids overwriting... they can still have any location)
    constraint.add_exactly_one(E, RoomType(TILES[0], "start"))
    constraint.add_exactly_one(E, RoomType(TILES[1], "end"))

    # Forces the starting tile to the center of the grid.
    center_coord = GRID_SIZE // 2
    start_loc = f"{center_coord},{center_coord}"

    """ Having trouble implementing the (only one tile per location) see below. please help :)"""

    for tile in REGULAR_TILES:
        constraint.add_exactly_one(E, RoomType(tile, "regular"))

    for tile in TILES[1:]:
        constraint.add_exactly_one(E, [OccupiedLocation(tile, loc) for loc in LOCATIONS])

    """ These two lines override the constraint forcing start to the center of the grid """
    for loc in LOCATIONS:
        constraint.add_at_most_one(E, [OccupiedLocation(tile, loc) for tile in TILES])

    constraint.add_exactly_one(E, OccupiedLocation(TILES[0], start_loc))







    #
    # E
    # for tile in TILES:
    #
    #     for loc in LOCATIONS:
    #         occ_loc = OccupiedLocation(tile, loc)
    #         constraint.add_exactly_one(E, occ_loc)
    #
    #         for adj_loc in calc_adj_locations(loc):
    #             for tile2 in TILES:
    #                 if tile != tile2 and loc != adj_loc:
    #                     occ_loc2 = OccupiedLocation(tile2, adj_loc[1])
    #                     constraint.add_at_least_one(E, Connected(occ_loc, occ_loc2, adj_loc[0]))
    # #
    #         for tile2 in TILES:
    #
    #             if tile != tile2:
    #                 for loc2 in LOCATIONS:

    # # hmm...
    # for occ_loc in occupied_locations:
    #     for occ_loc2 in occupied_locations.:
    #         constraint.add_at_least_one(E, [Connected(occ_loc, occ_loc2, d) for d in DIRECTIONS])

    """
    There must be only one OccupiedTile at a singular location
    Every OccupiedTile must be connected to at least one other OccupiedTile
    (Note): This doesn't fix islands. For that, we need to ensure every path can reach one another.
    """

    # Ensure no two tiles occupy the same location


def calc_adj_locations(loc):
    """
    Determines all valid adjacent locations to a given location.
    This will not include locations that are out of bounds.
    """

    adj_locs = []

    loc_data = loc.split(",")
    x = int(loc_data[0])
    y = int(loc_data[1])

    # Calculate N neighbor
    if y < GRID_SIZE - 1:
        adj_locs.append(['N', f"{x},{y+1}"])

    # Calculate S neighbor
    if 0 < y < GRID_SIZE:
        adj_locs.append(['S', f"{x},{y-1}"])

    # Calculate E neighbor
    if x < GRID_SIZE - 1:
        adj_locs.append(['E', f"{x+1},{y}"])

    if 0 < x < GRID_SIZE:
        adj_locs.append(['W', f"{x-1},{y}"])

    return adj_locs


def process_solution(solution):
    """Extract and format the relevant parts of a solution."""
    tile_locations = {tile: None for tile in TILES}
    tile_types = {}

    for var, value in solution.items():
        if value:  # Only process variables set to True
            # Check if the variable is a Location proposition
            if "Location(" in var._prop_name():
                # Extract tile and location from the proposition name
                parts = var._prop_name().split("(")[1].strip(")").split("@")
                tile, location = parts[0].strip(), parts[1].strip()
                tile_locations[tile] = location
            # Check if the variable is a RoomType proposition
            elif "RoomType(" in var._prop_name():
                parts = var._prop_name().split("(")[1].strip(")").split("=")
                tile, room_type = parts[0].strip(), parts[1].strip()
                tile_types[tile] = room_type

    # Output results in a readable format
    print("\nTile Locations:")
    for tile, location in tile_locations.items():
        print(f"  {tile} -> {location}")

    print("\nTile Types:")
    for tile, room_type in tile_types.items():
        print(f"  {tile} -> {room_type}")

    display.create_grid(tile_locations, tile_types)


def run_tests():
    apply_constraints()
    theory = E.compile()

    # Test satisfiability
    print("\nSatisfiable:", theory.satisfiable())

    # Sample and process a few solutions
    print("\nSample Solutions:")

    for i in range(1):  # Generate 3 random solutions to avoid long runtime TODO: THESE ARENT RANDOM. fix!!
        solution = theory.solve()

        print(f"\nSolution {i+1}:")
        process_solution(solution)


if __name__ == "__main__":
    run_tests()
