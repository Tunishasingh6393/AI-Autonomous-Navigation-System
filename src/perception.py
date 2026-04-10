import cv2
import numpy as np
from typing import List, Tuple

class Perception:
    def __init__(self):
        self.obstacle_threshold = 128
    
    def detect_obstacles(self, camera_feed: np.ndarray) -> List[Tuple[int, int]]:
        """
        Detect obstacles in camera feed using simple thresholding and contour detection.
        Returns relative positions of obstacles.
        """
        gray = cv2.cvtColor(camera_feed, cv2.COLOR_BGR2GRAY) if len(camera_feed.shape) == 3 else camera_feed
        _, thresh = cv2.threshold(gray, self.obstacle_threshold, 255, cv2.THRESH_BINARY)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        obstacles = []
        for cnt in contours:
            if cv2.contourArea(cnt) > 10:  # Filter small noise
                M = cv2.moments(cnt)
                if M['m00'] != 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    obstacles.append((cx, cy))
        return obstacles

