# dino.py
import pygame
from settings import *

class Dino:
    def __init__(self, x, y, screen_height):
        self.x = x
        self.y = screen_height - y + 10
        self.width = 40
        self.height = 60
        self.vel_y = 0
        self.jumping = False
        self.crouching = False
        self.original_y = self.y # this stores an original y for reference when standing up

    def jump(self):
        if not self.jumping:
            self.y = SCREEN_HEIGHT - self.height - 10
            self.jumping = True
            self.vel_y = -15  # Negative because in Pygame, y increases downwards

    def crouch(self):
        if not self.jumping:
            self.crouching = True
            height_difference = self.height - 30  # Calculate the difference in height
            self.y += height_difference  # Move the rectangle up
            self.height = 30

    def stand(self):
        if self.crouching:
            self.crouching = False
            height_difference = 60 - self.height  # Calculate how much to move back down
            self.y -= height_difference  # Move back to original position from the bottom
            self.height = 60

    def update(self):
        # Gravity
        if self.jumping:
            self.y += self.vel_y
            self.vel_y += 1  # Gravity effect
            
            # Stop jumping if hit the ground
            if self.y >= SCREEN_HEIGHT - self.height - 10:
                self.y = SCREEN_HEIGHT - self.height - 10
                self.jumping = False
                self.vel_y = 0

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), [self.x, self.y, self.width, self.height])