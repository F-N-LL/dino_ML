import pygame
import sys
import random
from settings import *
from dino import Dino
from obstacle import ObstaclesManager

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Run")
clock = pygame.time.Clock()

def calculate_speed_from_score(score):
    base_speed = INITIAL_SPEED
    speed_increment = 0.005                          # 🐱 GENERAL MOD SPEED BASED ON SCORE
    return base_speed + (score * speed_increment)

def restart_game(initial_score=0):
    global dino, obstacles_manager, score, speed
    dino = Dino(100, 80, SCREEN_HEIGHT)
    obstacles_manager = ObstaclesManager()
    score = initial_score
    speed = calculate_speed_from_score(score)

# Initialize game objects and variables
dino = None
obstacles_manager = None
score = 0
speed = INITIAL_SPEED
font = pygame.font.Font(None, 36)

speed_font_size = 24
speed_font = pygame.font.Font(None, speed_font_size)

def show_game_over_screen():
    game_over_font = pygame.font.Font(None, 74)
    restart_font = pygame.font.Font(None, 32)
    score_text = font.render(f"Score: {score}", True, (0, 0, 200))
    game_over_text = game_over_font.render("GAME OVER", True, (200, 0, 0))
    restart_text = restart_font.render("Press SPACE to restart or Q to quit", True, (0, 0, 200))

    screen.blit(game_over_text, [SCREEN_WIDTH//2 - game_over_text.get_width()//2, 
                                SCREEN_HEIGHT//2 - game_over_text.get_height()//2 - 20])
    screen.blit(restart_text, [SCREEN_WIDTH//2 - restart_text.get_width()//2, 
                              SCREEN_HEIGHT//2 + game_over_text.get_height()//2 - 10])
    screen.blit(score_text, [SCREEN_WIDTH//2 - score_text.get_width()//2, 
                            SCREEN_HEIGHT//2 + 100])

    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                elif event.key == pygame.K_SPACE:
                    return True

def game_loop(initial_score=0):
    global score, speed
    
    # Initialize game with specified starting score
    restart_game(initial_score)
    
    frame_counter = 0
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key in (pygame.K_UP, pygame.K_SPACE):
                    dino.jump()
                elif event.key == pygame.K_DOWN:
                    dino.crouch()
            elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                dino.stand()
        
        # Update speed based on current score
        speed = calculate_speed_from_score(score)
        
        obstacles_manager.update(SCREEN_WIDTH, speed, score)

        # Add obstacles with probability based on speed
        spawn_chance = int(max(100 - int(speed * 2), 70))  # Convert to int
        if random.randint(1, spawn_chance) == 1:
            obstacles_manager.add_obstacle(SCREEN_WIDTH, SCREEN_HEIGHT, speed, score)

        dino.update()
        
        screen.fill(WHITE)
        dino.draw(screen)
        obstacles_manager.draw(screen)
        
        # Increment score
        if frame_counter % 5 == 0:
            score += 1
        frame_counter += 1

        # Display score and speed
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        speed_text = speed_font.render(f"Speed: {speed:.4f}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(speed_text, (10, 50))

        if obstacles_manager.collide(dino):
            print("Collision detected! Game Over.")
            if not show_game_over_screen():
                running = False
            else:
                restart_game(0)  # Reset to beginning when restarting
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

# Start the game with a specific score (e.g., 600)
game_loop(1600)