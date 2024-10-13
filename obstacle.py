# obstacle.py
import pygame
import random
from settings import *

class Obstacle:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = (255, 0, 0)  # Red for visibility, can be changed or made variable

    def move(self):
        self.x -= self.speed  # Move the obstacle to the left

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class Cactus(Obstacle):
    def __init__(self, x, screen_height, speed):
        # Assume ground level with some offset, adjust as necessary
        ground_level = screen_height - 30  
        super().__init__(x, ground_level - 20, 20, 40, speed)  # Height adjusted to not reach below ground

class ObstaclesManager:
    def __init__(self):
        self.obstacles = []
        self.speed = INITIAL_SPEED

    def add_obstacle(self, screen_width, screen_height, speed):
        gap = random.randint(200, max(400 - (speed - INITIAL_SPEED) * 30, 200))
        if not self.obstacles or self.obstacles[-1].x < screen_width - gap:
            self.obstacles.append(Cactus(screen_width, screen_height, speed))

    def update(self, screen_width, speed):
        for obstacle in self.obstacles[:]:
            obstacle.move()
            if obstacle.x < -obstacle.width:
                self.obstacles.remove(obstacle)

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def collide(self, dino):
        for obstacle in self.obstacles:
            if (dino.x < obstacle.x + obstacle.width and 
                dino.x + dino.width > obstacle.x and
                dino.y + dino.height > obstacle.y):
                return True
        return False