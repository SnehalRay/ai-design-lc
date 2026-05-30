'''
2069. Walking Robot Simulation II

A width x height grid is on an XY-plane with the bottom-left cell at (0, 0) and the top-right cell at (width - 1, height - 1). The grid is aligned with the four cardinal directions ("North", "East", "South", and "West"). A robot is initially at cell (0, 0) facing direction "East".

The robot can be instructed to move for a specific number of steps. For each step, it does the following.

Attempts to move forward one cell in the direction it is facing.
If the cell the robot is moving to is out of bounds, the robot instead turns 90 degrees counterclockwise and retries the step.
After the robot finishes moving the number of steps required, it stops and awaits the next instruction.

Implement the Robot class:

Robot(int width, int height) Initializes the width x height grid with the robot at (0, 0) facing "East".
void step(int num) Instructs the robot to move forward num steps.
int[] getPos() Returns the current cell the robot is at, as an array of length 2, [x, y].
String getDir() Returns the current direction of the robot, "North", "East", "South", or "West".
'''

from enum import Enum
from typing import List

class Direction(Enum):
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)
    NORTH = (-1, 0)

class Robot:
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.pos = [0, 0]
        self.dir_idx = 0
        self.directions = [Direction.EAST, Direction.SOUTH, Direction.WEST, Direction.NORTH]

    def step(self, num: int) -> None:
        num %= 2 * (self.width + self.height - 2)
        for _ in range(num):
            for _ in range(4):
                dx, dy = self.directions[self.dir_idx].value
                nx, ny = self.pos[0] + dx, self.pos[1] + dy
                if 0 <= nx < self.height and 0 <= ny < self.width:
                    self.pos = [nx, ny]
                    break
                self.dir_idx = (self.dir_idx + 1) % 4

    def get_position(self) -> List[int]:
        return self.pos

    def get_direction(self) -> Direction:
        return self.directions[self.dir_idx]

robot = Robot(4,4)
print(robot.get_position())
print(robot.get_direction())
robot.step(16) 
print(robot.get_position())
print(robot.get_direction())

