#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.media.ev3dev import SoundFile, ImageFile

import robotlib
# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

import constants

ev3 = EV3Brick()
left_motor = Motor(Port.A)
right_motor = Motor(Port.D)

# Manhattan distance grid
grid = [[float('inf') for _ in range(constants.num_cols)] for _ in range(constants.num_rows)]
# Obstacle map: 2D grid - 0 for free space and 1 for obstacle
obstacle_map = [[0 for _ in range(constants.num_cols)] for _ in range(constants.num_rows)]

# Get starting and goal coordinates from constants, and convert to 2D array coordinates for path planning
start_coords = (round(constants.start[0] / 0.305) - 1, round(constants.start[1] / 0.305) - 1)
goal_coords = (round(constants.goal[0] / 0.305) - 1, round(constants.goal[1] / 0.305) - 1)
print("start:", start_coords)
print("goal:", goal_coords)

# flooded stores whether a certain cell is already visited during BFS flooding for Manhattan Distance
flooded = [[False for _ in range(constants.num_cols)] for _ in range(constants.num_rows)]

# BFS using a queue to visit every reachable cell from the goal and mark its distance
def flood_manhattan(grid, x_begin, y_begin, dist):
    frontier = [(x_begin, y_begin), None] # None marks the end of a level in BFS
    while len(frontier) > 0:
        if frontier[0] == None:
            dist += 1
            frontier.pop(0)
            frontier.append(None)
            if frontier[0] == None:
                break
        else:
            x, y = frontier.pop(0)
            # print("Popped:", x, y)
            if not flooded[x][y]:
                if not obstacle_map[x][y]:
                    grid[x][y] = dist
                flooded[x][y] = True
                                                                                                                                                                                                                        
            if not obstacle_map[x][y]:
                neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                for x_n, y_n in neighbors:
                    if 0 <= x_n < constants.num_rows and 0 <= y_n < constants.num_cols and not flooded[x_n][y_n] and (x_n, y_n) not in frontier:
                        frontier.append((x_n, y_n))

for obstacle in constants.obstacles:
    x, y = obstacle
    x = round(x / 0.305) - 1
    y = round(y / 0.305) - 1
    obstacle_map[x][y] = 1
    grid[x][y] = float('inf')


flood_manhattan(grid, goal_coords[0], goal_coords[1], 0)

for i in range(constants.num_rows):
    for j in range(constants.num_cols):
        print(grid[i][j], end="  ")


print("Obstacle map:")
for row in obstacle_map:
    for item in row:
        print(item, end=' ')
    print()

print("Grid:")
for row in grid:
    for item in row:
        print("%4s"% (str(item),), end=' ')
    print()

orientation = constants.orientation
print("Orientation:", orientation)
position = start_coords

x, y = position

path = ''

if grid[x][y] != float('inf'):
    while grid[x][y] != 0:
        x_front = x
        y_front = y
        if orientation == 1:
            x_front += 1
        elif orientation == -1:
            x_front -= 1
        elif orientation == 1j:
            y_front += 1
        else:
            y_front -= 1
        
        if 0 <= x_front < constants.num_rows and 0 <= y_front < constants.num_cols and grid[x_front][y_front] < grid[x][y]:
            path += 'F'
            x, y = x_front, y_front
            print(path, x, y)
        else:
            path += 'L'
            print(path, x, y)
            orientation *= 1j 
    
    path = path.replace('LLL', 'R')
    print(path)

    # Execute path:
    while(len(path) > 0):
        if path[0] == 'F':
            count = 1
            while count < len(path) and path[count] == 'F':
                count += 1
            print("Move forward", count, "times.")
            robotlib.moveDistanceGyro(count * 30.5, left_motor, right_motor)
            path = path[count:]
        elif path[0] == 'L':
            print("Turn left 90 degrees.")
            robotlib.turn(90, left_motor, right_motor)
            path = path[1:]
        else:
            print("Turn right 90 degrees.")
            robotlib.turn(-90, left_motor, right_motor)
            path = path[1:]
    
else:
    ev3.speaker.say("No path exists!")

