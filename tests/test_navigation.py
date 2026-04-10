import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import numpy as np
from src.path_planning import AStarPlanner
from src.navigation import Navigation

def test_a_star():
    grid = np.zeros((10, 10))
    grid[5,5] = 1  # obstacle
    planner = AStarPlanner(grid)
    path = planner.plan((0,0), (9,9))
    assert path is not None
    print("A* test passed!")

def test_nav():
    grid = np.zeros((10,10))
    planner = AStarPlanner(grid)
    nav = Navigation(grid, planner)
    next_pos = nav.navigate_to_goal(np.array([0,0]), np.array([9,9]), [])
    assert next_pos != (0,0)
    print("Navigation test passed!")

if __name__ == "__main__":
    test_a_star()
    test_nav()

