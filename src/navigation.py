import time
from typing import List, Tuple
import numpy as np

class Navigation:
    def __init__(self, sim_grid, planner):
        self.grid = sim_grid
        self.planner = planner
    
    def navigate_to_goal(self, sim_agent_pos, sim_goal_pos, perception_obs) -> Tuple[int, int]:
        """
        Use path planning and perception to decide next move.
        """
        path = self.planner.plan(tuple(sim_agent_pos), tuple(sim_goal_pos))
        if path and len(path) > 1:
            next_pos = path[1]
            # Simple local avoidance using perception
            rel_obs = [(ox - 5, oy - 5) for ox, oy in perception_obs]  # Relative to view center
            for dx, dy in rel_obs:
                if abs(dx) < 3 and abs(dy) < 3 and dx != 0 and dy != 0:
                    # Avoid local obstacle
                    next_pos = (sim_agent_pos[0] + np.sign(sim_goal_pos[0] - sim_agent_pos[0]), 
                                sim_agent_pos[1] + np.sign(sim_goal_pos[1] - sim_agent_pos[1]))
                    break
            return next_pos
        else:
            # Default move towards goal
            dx = 1 if sim_goal_pos[0] > sim_agent_pos[0] else -1 if sim_goal_pos[0] < sim_agent_pos[0] else 0
            dy = 1 if sim_goal_pos[1] > sim_agent_pos[1] else -1 if sim_goal_pos[1] < sim_agent_pos[1] else 0
            return (sim_agent_pos[0] + dx, sim_agent_pos[1] + dy)

