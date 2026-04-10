import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simulation import Simulation
from perception import Perception
from path_planning import AStarPlanner
from navigation import Navigation
import pygame

def main():
    sim = Simulation()
    perception = Perception()
    planner = AStarPlanner(sim.grid)
    nav = Navigation(sim.grid, planner)
    
    running = True
    path = None
    
    while running:
        running = sim.run_step()
        if not running:
            break
        
        # Perception
        camera_feed = sim.get_camera_feed()
        obstacles = perception.detect_obstacles(camera_feed)
        
        # Plan path
        path = planner.plan(tuple(sim.agent_pos), tuple(sim.goal_pos))
        
        # Navigate
        if path:
            next_pos = nav.navigate_to_goal(sim.agent_pos, sim.goal_pos, obstacles)
            sim.update_agent(next_pos)
        
        # Check goal
        if sim.is_goal_reached():
            print("Goal reached!")
            pygame.time.wait(2000)
            break
        
        sim.render()
    
    pygame.quit()
    print("Simulation completed.")

if __name__ == "__main__":
    main()

