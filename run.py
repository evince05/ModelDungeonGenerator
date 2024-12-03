from bauhaus import Encoding, proposition, constraint, Or
from nnf import config

import visuals.solution_display as display

# Use a faster SAT solver
config.sat_backend = "kissat"

# Encoding for the full-sized test
E = Encoding()

# Constants for the full problem size
NUM_TILES = 5  # 1 start, 1 end, 3 regular tiles
GRID_SIZE = 5  # 5x5 grid

TILES = [f"t{i}" for i in range(NUM_TILES)]
SPECIAL_TILES = ["start", "end"]


REGULAR_TILES = TILES[2:]  # Exclude start and end
LOCATIONS = [f"{row},{col}" for row in range(GRID_SIZE) for col in range(GRID_SIZE)]
CENTER_LOCATION = f"{GRID_SIZE // 2},{GRID_SIZE // 2}"

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
class Location:
    def __init__(self, tile, location):
        assert tile in TILES
        assert location in LOCATIONS
        self.tile = tile
        self.location = location

    def _prop_name(self):
        return f"Location({self.tile}@{self.location})"

@proposition(E)
class Adjacent:
    def __init__(self, tile1, tile2):
        assert tile1 in TILES
        assert tile2 in TILES
        self.tile1 = tile1
        self.tile2 = tile2

    def _prop_name(self):
        return f"Adjacent({self.tile1}-{self.tile2})"

def get_adjacent_locations(location):
    """Returns a list of locations adjacent to the given location."""
    row, col = map(int, location.split(","))
    adjacent = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        adj_row, adj_col = row + dr, col + dc
        if 0 <= adj_row < GRID_SIZE and 0 <= adj_col < GRID_SIZE:
            adjacent.append(f"{adj_row},{adj_col}")
    return adjacent

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

    # Ensure all other tiles are regular
    for tile in REGULAR_TILES:
        constraint.add_exactly_one(E, RoomType(tile, "regular"))

    # Ensure each tile is placed in exactly one location
    for tile in TILES:
        constraint.add_exactly_one(E, [Location(tile, loc) for loc in LOCATIONS])

    # Ensure no two tiles occupy the same location
    for loc in LOCATIONS:
        constraint.add_at_most_one(E, [Location(tile, loc) for tile in TILES])

    # Start tile must be in the center of the grid
    constraint.add_exactly_one(E, [Location(TILES[0], CENTER_LOCATION)])

    # Enforce adjacency constraints
    for tile1 in TILES:
        for tile2 in TILES:
            if tile1 != tile2:
                # If two tiles are adjacent, their locations must also be adjacent
                for loc1 in LOCATIONS:
                    adj_locs = get_adjacent_locations(loc1)
                    constraint.add_implies_all(
                        E,
                        Adjacent(tile1, tile2),
                        Or([Location(tile1, loc1) & Location(tile2, adj) for adj in adj_locs])
                    )

    # Each tile must have at least 1 and at most 2 adjacent tiles, except start and end tiles
    for tile in REGULAR_TILES:
        adjacent_constraints = [Adjacent(tile, other) for other in TILES if other != tile]
        constraint.add_at_least_one(E, adjacent_constraints)
        constraint.add_at_most_k(E, 2, adjacent_constraints)

    # Start and end tiles must have exactly one adjacent tile
    start_adj_constraints = [Adjacent(TILES[0], other) for other in TILES if other != TILES[0]]
    end_adj_constraints = [Adjacent(TILES[1], other) for other in TILES if other != TILES[1]]

    constraint.add_exactly_one(E, start_adj_constraints)
    constraint.add_exactly_one(E, end_adj_constraints)

def process_solution(solution):
    """Extract and format the relevant parts of a solution."""
    tile_locations = {tile: None for tile in TILES}
    tile_types = {}

    for var, value in solution.items():
        if value:  # Only process variables set to True
            var_str = str(var)
            # Check if the variable is a Location proposition
            if "Location(" in var_str:
                # Extract tile and location from the string representation
                parts = var_str.split("(")[1].strip(")").split("@")
                tile, location = parts[0].strip(), parts[1].strip()
                tile_locations[tile] = location
            # Check if the variable is a RoomType proposition
            elif "RoomType(" in var_str:
                parts = var_str.split("(")[1].strip(")").split("=")
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
    for i in range(3):  # Generate 3 random solutions to avoid long runtime
        solution = theory.solve()
        if solution:
            print(f"\nSolution {i+1}:")
            process_solution(solution)
        else:
            print(f"\nNo solution found for attempt {i+1}")

if __name__ == "__main__":
    run_tests()