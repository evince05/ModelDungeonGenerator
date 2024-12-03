from bauhaus import Encoding, proposition, constraint, Or
from nnf import config

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
        self.tile = tile
        self.room_type = room_type

    def _prop_name(self):
        return f"RoomType({self.tile}={self.room_type})"

@proposition(E)
class Location:
    def __init__(self, tile, location):
        self.tile = tile
        self.location = location

    def _prop_name(self):
        return f"Location({self.tile}@{self.location})"

@proposition(E)
class Adjacent:
    def __init__(self, tile1, tile2):
        self.tile1 = tile1
        self.tile2 = tile2

    def _prop_name(self):
        return f"Adjacent({self.tile1}-{self.tile2})"

def get_adjacent_locations(location):
    row, col = map(int, location.split(","))
    adjacent = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        adj_row, adj_col = row + dr, col + dc
        if 0 <= adj_row < GRID_SIZE and 0 <= adj_col < GRID_SIZE:
            adjacent.append(f"{adj_row},{adj_col}")
    return adjacent

def apply_constraints():
    # Room type constraints
    constraint.add_exactly_one(E, [RoomType(TILES[0], "start")])
    constraint.add_exactly_one(E, [RoomType(TILES[1], "end")])
    for tile in REGULAR_TILES:
        constraint.add_exactly_one(E, [RoomType(tile, "regular")])

    # Location constraints
    for tile in TILES:
        constraint.add_exactly_one(E, [Location(tile, loc) for loc in LOCATIONS])
    for loc in LOCATIONS:
        constraint.add_at_most_one(E, [Location(tile, loc) for tile in TILES])

    # Start tile in center
    constraint.add_exactly_one(E, [Location(TILES[0], CENTER_LOCATION)])

    # Adjacency constraints
    for tile1 in TILES:
        for tile2 in TILES:
            if tile1 != tile2:
                for loc1 in LOCATIONS:
                    adj_locs = get_adjacent_locations(loc1)
                    constraint.add_implies_all(
                        E,
                        Adjacent(tile1, tile2),
                        Or([Location(tile1, loc1) & Location(tile2, adj) for adj in adj_locs])
                    )

    # Regular tiles must have exactly 2 adjacent tiles
    for tile in REGULAR_TILES:
        adjacent_constraints = [Adjacent(tile, other) for other in TILES if other != tile]
        constraint.add_exactly_k(E, 2, adjacent_constraints)

    # Start and end tiles must have exactly one adjacent tile
    for special_tile in [TILES[0], TILES[1]]:
        adj_constraints = [Adjacent(special_tile, other) for other in TILES if other != special_tile]
        constraint.add_exactly_one(E, adj_constraints)

    # Ensure connectivity
    for i in range(1, len(TILES)):
        constraint.add_implies_all(
            E,
            Adjacent(TILES[i-1], TILES[i]),
            Or([Adjacent(TILES[i-1], TILES[j]) & Adjacent(TILES[j], TILES[i]) for j in range(len(TILES)) if j != i-1 and j != i])
        )

def process_solution(solution):
    tile_locations = {tile: None for tile in TILES}
    tile_types = {}

    for var, value in solution.items():
        if value:
            var_str = str(var)
            if "Location(" in var_str:
                parts = var_str.split("(")[1].strip(")").split("@")
                tile, location = parts[0].strip(), parts[1].strip()
                tile_locations[tile] = location
            elif "RoomType(" in var_str:
                parts = var_str.split("(")[1].strip(")").split("=")
                tile, room_type = parts[0].strip(), parts[1].strip()
                tile_types[tile] = room_type

    return tile_locations, tile_types

def create_grid(tile_locations, tile_types):
    grid = [['X' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for tile, location in tile_locations.items():
        row, col = map(int, location.split(','))
        if tile_types[tile] == 'start':
            grid[row][col] = 'S'
        elif tile_types[tile] == 'end':
            grid[row][col] = 'E'
        else:
            grid[row][col] = 'R'
    return grid

def print_grid(grid):
    print("--------------------")
    for row in grid:
        print(' '.join(row))
    print("--------------------")

def run_tests():
    apply_constraints()
    theory = E.compile()
    print("\nSatisfiable:", theory.satisfiable())

    print("\nSample Solutions:")
    for i in range(3):
        solution = theory.solve()
        if solution:
            print(f"\nSolution {i+1}:")
            tile_locations, tile_types = process_solution(solution)
            grid = create_grid(tile_locations, tile_types)
            print_grid(grid)
        else:
            print(f"\nNo solution found for attempt {i+1}")

if __name__ == "__main__":
    run_tests()