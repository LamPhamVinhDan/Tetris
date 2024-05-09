import pygame
import sys
from game import Game
from tetris_two_players import *

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Font settings
font = pygame.font.Font(None, 36)

# Function to display menu
def display_menu(screen):
    screen.fill(WHITE)
    title_text = font.render("Tetris Menu", True, BLACK)
    single_player_text = font.render("1. Single Player", True, BLACK)
    two_players_text = font.render("2. Two Players", True, BLACK)

    screen.blit(title_text, (100, 50))
    screen.blit(single_player_text, (100, 150))
    screen.blit(two_players_text, (100, 200))

    pygame.display.flip()

# Main function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris Menu")

    while True:
        display_menu(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    Game()
                elif event.key == pygame.K_2:
                    main()

if __name__ == "__main__":
    main()