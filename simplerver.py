from bauhaus import Encoding, proposition, constraint
from nnf import config

# docker run -it -v "C:\Users\paulz\Documents\ModelDungeonGenerator:/PROJECT" cisc204 /bin/bash -c "python3 simplerver.py"

# Use a faster SAT solver
config.sat_backend = "kissat"

# Encoding for the test
E = Encoding()

# Constants for the 7-tile version
NUM_TILES = 2  # 1 start, 1 end, 5 regular tiles
GRID_SIZE = 10  # Smaller 5x5 grid

TILES = [f"t{i}" for i in range(NUM_TILES)]
SPECIAL_TILES = ["start", "end"]
REGULAR_TILES = TILES[2:]  # Exclude start and end
LOCATIONS = [f"l_{row},{col}" for row in range(GRID_SIZE) for col in range(GRID_SIZE)]


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


def apply_constraints():
    # Ensure exactly one start and one end tile
    constraint.add_exactly_one(E, [RoomType(tile, "start") for tile in TILES])
    constraint.add_exactly_one(E, [RoomType(tile, "end") for tile in TILES])

    # Ensure all other tiles are regular
    for tile in REGULAR_TILES:
        constraint.add_exactly_one(E, [RoomType(tile, "regular")])

    # Ensure each tile is placed in exactly one location
    for tile in TILES:
        constraint.add_exactly_one(E, [Location(tile, loc) for loc in LOCATIONS])

    # Ensure no two tiles occupy the same location
    for loc in LOCATIONS:
        constraint.add_at_most_one(E, [Location(tile, loc) for tile in TILES])


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


def run_tests():
    apply_constraints()
    theory = E.compile()

    # Test satisfiability
    print("\nSatisfiable:", theory.satisfiable())

    # Output one solution
    print("\nSolution:")
    solution = theory.solve()  # Only generate one solution
    process_solution(solution)


if __name__ == "__main__":
    run_tests()
