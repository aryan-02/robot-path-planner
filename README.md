# robot-path-planner
A Potential Field based Path Planner Robot using Micropython on Lego Mindstorms EV3. A project for CSE 4360 (Autonomous Robot Design and Programming)

This was a team project I worked on for my Robotics class.

## Task Description
The task involved building a robot using the
Lego Mindstorms EV3 platform and programming a path planner to get the
robot from a start coordinate to a goal. The coordinates for start, goal and
obstacles are expected to be hardcoded before robot runs.

## Solution Implementation
This solution for the problem uses a Potential Field based approach. We use Manhattan Distance from the goal as our potential function. It involves discretizing the workspace into a grid. Assuming each obstacle cell is marked, we flood-fill the grid using Breadth First Search (BFS) with the Manhattan distances from the goal. The path planning algorithm then reduces to moving along the decreasing direction of the Manhattan Distance values.

![algorithm](https://github.com/aryan-02/robot-path-planner/assets/29256761/5d894168-0316-4d08-bda8-99249a6bc817)

