import pygame
import numpy as np
import cv2
from typing import Tuple, List

class Simulation:
    def __init__(self, width: int = 800, height: int = 600, cell_size: int = 20):
        pygame.init()
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid_width = width // cell_size
        self.grid_height = height // cell_size
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('AI Autonomous Navigation Simulation')
        self.clock = pygame.time.Clock()
        self.grid = np.zeros((self.grid_height, self.grid_width), dtype=int)  # 0: free, 1: obstacle
        self.agent_pos = np.array([1, 1], dtype=int)
        self.goal_pos = np.array([self.grid_width-2, self.grid_height-2], dtype=int)
        self._add_obstacles()
    
    def _add_obstacles(self):
        # Add some random obstacles
        num_obs = 50
        h, w = self.grid.shape
        for _ in range(num_obs):
            x = np.random.randint(2, w-2)
            y = np.random.randint(2, h-2)
            self.grid[y, x] = 1
    
    def get_camera_feed(self) -> np.ndarray:
        # Simulate camera view: crop around agent
        view_size = 10
        x, y = self.agent_pos
        crop_y = slice(max(0, y-view_size), min(self.grid_height, y+view_size+1))
        crop_x = slice(max(0, x-view_size), min(self.grid_width, x+view_size+1))
        view = self.grid[crop_y, crop_x].astype(np.uint8) * 255
        view = cv2.resize(view, (100, 100))
        return view
    
    def update_agent(self, new_pos: Tuple[int, int]):
        nx, ny = new_pos
        if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height and self.grid[ny, nx] == 0:
            self.agent_pos = np.array([nx, ny])
    
    def is_goal_reached(self) -> bool:
        return np.array_equal(self.agent_pos, self.goal_pos)
    
    def render(self):
        self.screen.fill((0, 0, 0))
        # Draw grid
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                color = (128, 128, 128) if self.grid[y, x] == 1 else (0, 100, 0)
                pygame.draw.rect(self.screen, color, (x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size))
        # Agent
        pygame.draw.circle(self.screen, (0, 255, 0), (self.agent_pos[0]*self.cell_size + self.cell_size//2, self.agent_pos[1]*self.cell_size + self.cell_size//2), self.cell_size//2)
        # Goal
        pygame.draw.circle(self.screen, (255, 0, 0), (self.goal_pos[0]*self.cell_size + self.cell_size//2, self.goal_pos[1]*self.cell_size + self.cell_size//2), self.cell_size//2)
        pygame.display.flip()
    
    def run_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        self.clock.tick(10)
        return True

