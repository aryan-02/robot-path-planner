num_rows = 15
num_cols = 10

# obstacle_builder = [(1, 2), (2, 2), (1, 1), (2, 1), (2, 8), (2, 7), (5, 6), (5, 5), (5, 4), (8, 8), (8, 2), (9, 2), (10, 2)]
# obstacle_builder = [(4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9), (7, 10), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7), (11, 3), (12, 4)]
obstacle_builder = [(4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9), (7, 10), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7), (11, 3), (12, 3), (12, 4), (13, 3), (13, 4)]
obstacles = [(i * 0.305, j * 0.305) for i, j in obstacle_builder]
# obstacles = [(i * 0.305, 3 * 0.305) for i in range(num_rows)]
print("Obstacles:", obstacles)

# start = (0.305, 1.525)
# goal = (2.745, 1.525)

start = (2 * 0.305, 2 * 0.305)
goal = (13 * 0.305, 7 * 0.305)

orientation = 1j

# Orientation =   1: facing positive x axis
# Orientation =  1j: facing positive y axis
# Orientation =  -1: facing negative x axis
# Orientation = -1j: facing negative y-axis