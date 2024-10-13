# main.py
import pygame
import sys
import random
from settings import *
from dino import Dino
from obstacle import ObstaclesManager

pygame.init()

# Used settings for screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Run")
clock = pygame.time.Clock()

dino = Dino(100, 80, SCREEN_HEIGHT)

# Initialize score
score = 0
font = pygame.font.Font(None, 36)  # Font for displaying score

speed = INITIAL_SPEED
obstacles_manager = ObstaclesManager()

def show_game_over_screen():
    game_over_font = pygame.font.Font(None, 74)
    restart_font = pygame.font.Font(None, 32)
    score_text = font.render(f"Score: {score}", True, (0, 0, 200))
    game_over_text = game_over_font.render("GAME OVER", True, (200, 0, 0))
    restart_text = restart_font.render("Press SPACE to restart or Q to quit", True, (0, 0, 200))

    # Adjust the y-coordinate of game_over_text to move it up
    screen.blit(game_over_text, [SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - game_over_text.get_height()//2 - 20])  # Adjusted y-coordinate
    
    # Adjust the y-coordinate of restart_text to move it up
    screen.blit(restart_text, [SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + game_over_text.get_height()//2 - 10])  # Adjusted y-coordinate
    
    # Adjust the y-coordinate of score_text to move it up
    screen.blit(score_text, [SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2 + 100])  # Adjusted y-coordinate

    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Exit the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False  # Quit the game
                elif event.key == pygame.K_SPACE:
                    return True   # Restart the game
    
def restart_game():
    global dino, obstacles_manager, score, speed
    dino = Dino(100, 80, SCREEN_HEIGHT)  # Reset Dino
    obstacles_manager = ObstaclesManager()  # Reset obstacles
    score = 0
    speed = INITIAL_SPEED

def game_loop():
    global score, speed
    frame_counter = 0
    speed_increase_interval = 600
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    dino.jump()
                elif event.key == pygame.K_SPACE:
                    dino.jump()
                elif event.key == pygame.K_DOWN:
                    dino.crouch()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    dino.stand()
        
        obstacles_manager.update(SCREEN_WIDTH, speed)  # Update obstacles

        # Increase speed logic
        frame_counter += 1
        if frame_counter % speed_increase_interval == 0:
            speed += 1

        # Adds obtacles randomly    
        if random.randint(1, 100) == 1:
            obstacles_manager.add_obstacle(SCREEN_WIDTH, SCREEN_HEIGHT, speed)
           #print(f"Obstacle added at {SCREEN_WIDTH}")  # Check if obstacles are being added

        #print(f"Obstacles on screen: {len(obstacles_manager.obstacles)}")  # Check number of obstacles each frame
        
        # Update dino's position
        dino.update() 
        
        screen.fill(WHITE)
        dino.draw(screen)  # Draw dino
        obstacles_manager.draw(screen)  # Draw obstacles
        
        # Increment score every 5 frames
        # frame_counter += 1
        # if frame_counter == 5:
        #     score += 1  # Increment score every 5 frames
        #     frame_counter = 0  # Reset counter

        # Increment and display score every 5 frames --- OTHER ALTERNATIVE
        if frame_counter % 5 == 0:
            score += 1

        # Display score
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))  # Position the score text at top-left corner


        if obstacles_manager.collide(dino):
            print("Collision detected! Game Over.")
            if not show_game_over_screen():  # Show game over screen
                running = False  # User chose to quit
            else:
                restart_game()  # User chose to restart
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

game_loop()