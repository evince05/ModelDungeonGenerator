class Tile:
    def __init__(self, x, y, room_type="regular"):
        self.position = (x, y)
        self.room_type = room_type
        # Neighbor nodes (north, east, south, west)
        self.neighbors = {'north': None, 'east': None, 'south': None, 'west': None}

    def set_neighbor(self, direction, neighbor_tile):
        if direction in self.neighbors:
            self.neighbors[direction] = neighbor_tile

    def __repr__(self):
        return f"Tile({self.position}, type={self.room_type})"

# Initialize a 25x25 grid with None placeholders
grid_size = 25
grid = [[None for _ in range(grid_size)] for _ in range(grid_size)]

# Define the starting tile's position at the center
start_x = start_y = grid_size // 2

# Populate the grid with Tile objects
for x in range(grid_size):
    for y in range(grid_size):
        # Set room type as 'start' for the center tile, others as 'regular'
        room_type = 'start' if (x, y) == (start_x, start_y) else 'regular'
        grid[x][y] = Tile(x, y, room_type)

# Connect neighboring tiles
for x in range(grid_size):
    for y in range(grid_size):
        tile = grid[x][y]
        if x > 0:  # North neighbor
            tile.set_neighbor('north', grid[x-1][y])
        if y < grid_size - 1:  # East neighbor
            tile.set_neighbor('east', grid[x][y+1])
        if x < grid_size - 1:  # South neighbor
            tile.set_neighbor('south', grid[x+1][y])
        if y > 0:  # West neighbor
            tile.set_neighbor('west', grid[x][y-1])

# Example usage
# Print center tile and its neighbors
center_tile = grid[start_x][start_y]
print("Center Tile:", center_tile)
print("Neighbors:", center_tile.neighbors)

# Set different room types
set_room_type(grid, start_x, start_y, "start")
set_room_type(grid, start_x, start_y + 1, "treasure")
set_room_type(grid, start_x - 1, start_y, "trap")
set_room_type(grid, start_x, start_y - 1, "end")

# Example usage
# Print the center tile and its neighbors with their types
center_tile = grid[start_x][start_y]
print("Center Tile:", center_tile)
for direction, neighbor in center_tile.neighbors.items():
    if neighbor:
        print(f"{direction.capitalize()} Neighbor:", neighbor)
