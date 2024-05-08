import pygame, sys
from game import Game
from colors import Colors

pygame.init()

# Set up fonts and surfaces for text display
title_font = pygame.font.Font(None, 40)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)

# Set up rectangles for positioning text elements
score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)

# Set up the Pygame display window
screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Python Tetris")

# Set up the Pygame clock
clock = pygame.time.Clock()

# Create a Game instance
game = Game()

# Set up a custom Pygame event for game updates
GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)

# Main game loop
while True:
    # Event handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game.game_over == True:
                game.game_over = False
                game.reset()
            if event.key == pygame.K_LEFT and game.game_over == False:
                game.move_left()
            if event.key == pygame.K_RIGHT and game.game_over == False:
                game.move_right()
            if event.key == pygame.K_DOWN and game.game_over == False:
                game.move_down()
                game.update_score(0, 1)
            if event.key == pygame.K_UP and game.game_over == False:
                game.rotate()
        if event.type == GAME_UPDATE and game.game_over == False:
            game.move_down()

    # Drawing loop
    # Render and display the score
    score_value_surface = title_font.render(str(game.score), True, Colors.white)
    screen.fill(Colors.dark_blue)
    screen.blit(score_surface, (365, 20, 50, 50))
    screen.blit(next_surface, (375, 180, 50, 50))

    # If the game is over, display the "GAME OVER" message
    if game.game_over == True:
        screen.blit(game_over_surface, (320, 450, 50, 50))

    # Draw the score rectangle and the score value
    pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
    screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx,
                                                                   centery=score_rect.centery))

    # Draw the next block rectangle and the next block preview
    pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
    game.draw(screen)

    # Update the display
    pygame.display.update()
    clock.tick(60)