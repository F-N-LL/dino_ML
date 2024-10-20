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
        self.color = (255, 0, 0)  # Red for visibility

    def move(self):
        self.x -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class Cactus(Obstacle):
    def __init__(self, x, screen_height, speed):
        ground_level = screen_height - 30
        super().__init__(x, ground_level - 20, 20, 40, speed)

class Bird(Obstacle):
    def __init__(self, x, screen_height, speed):
        flying_levels = [screen_height - 150, screen_height - 100, screen_height - 50]
        flying_level = random.choice(flying_levels)
        super().__init__(x, flying_level, 30, 30, speed)
        self.color = (255, 165, 0)

class ObstaclesManager:
    def __init__(self):
        self.obstacles = []
        self.speed = INITIAL_SPEED

    # def get_max_cacti_count(self, score):
    #     if score < 2500:
    #         return min(2, 1 + score // 1000)  # Start with 1, max 2 before 2500
    #     else:
    #         return 4  # Allow up to 4 cacti after 2500 points
    
    def get_max_cacti_count(self, score):
        if score < 200:
            return 1  # Only 1 cactus up to 200 points
        elif score < 600:
            return 2  # Up to 2 cacti between 200-600 points
        elif score < 1500:
            return 3  # Up to 3 cacti between 600-1500 points
        else:
            return 4  # 4 cacti allowed after 1500 points

    def add_obstacle(self, screen_width, screen_height, speed, score):
        min_gap = 100
        max_gap = max(400 - (speed - INITIAL_SPEED) * 30, 200)
        gap_reduction = min(score // 100, max_gap - min_gap)
        gap = random.randint(min_gap, max_gap - gap_reduction)
        
        if not self.obstacles or self.obstacles[-1].x < screen_width - gap:
            if random.choice([True, False]):  # 50% chance of either Cactus or Bird
                if random.random() < 0.3:  # 30% chance to spawn a group of cacti
                    max_cacti = self.get_max_cacti_count(score)
                    num_cacti = random.randint(1, max_cacti)  # Number of cacti based on score
                    
                    # Calculate spacing between cacti based on score
                    spacing = 30 if score < 1000 else 25  # Tighter spacing at higher scores
                    
                    for i in range(num_cacti):
                        self.obstacles.append(Cactus(screen_width + i * spacing, screen_height, speed))
                else:
                    self.obstacles.append(Cactus(screen_width, screen_height, speed))
            else:
                # Birds become more common at higher scores
                if score > 1500 or random.random() < 0.4:  # 40% chance initially, more frequent later
                    self.obstacles.append(Bird(screen_width, screen_height, speed))
                else:
                    self.obstacles.append(Cactus(screen_width, screen_height, speed))

    def update(self, screen_width, speed, score):
        for obstacle in self.obstacles[:]:
            obstacle.move()
            if obstacle.x < -obstacle.width:
                self.obstacles.remove(obstacle)
        
        # Gradually increase speed based on score
        if score % 100 == 0:
            self.speed += 0.1

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def collide(self, dino):
        for obstacle in self.obstacles:
            if (dino.x < obstacle.x + obstacle.width and 
                dino.x + dino.width > obstacle.x and
                dino.y < obstacle.y + obstacle.height and
                dino.y + dino.height > obstacle.y):
                return True
        return False
