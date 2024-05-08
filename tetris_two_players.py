"""
Tetris Duel: A Tetris game with versus mode

This program implements a Tetris game with a versus mode where two players compete against each other.
Each player has their own game grid and controls a set of Tetris blocks.
The players aim to clear lines to send garbage lines to their opponent's grid.
The game ends when a player's grid is filled up to the top.

Classes:
    Grid: Represents the game grid for each player.
    Game: Manages the main game logic and interactions.
    Position: Represents a position (row, column) on the game grid.
    Block: Base class for Tetris blocks.
    IBlock, JBlock, LBlock, OBlock, SBlock, TBlock, ZBlock: Subclasses representing different Tetris blocks.

Functions:
    main(): Main function to run the game.

Usage:
    - Run the program to start the Tetris Duel game.
    - Player 1 uses arrow keys for movement and the space bar to rotate blocks.
    - Player 2 controls are not implemented in this version but can be added similarly to Player 1.

Dependencies:
    - Pygame library for graphics and event handling.
    - Colors module for defining colors used in the game.
"""
import pygame
import sys
import random
from colors import Colors
from block import Block
from position import Position

# Class for the game grid
class Grid:
    def __init__(self, num_rows, num_cols, cell_size):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size = cell_size
        self.grid = [[0 for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        self.colors = Colors.get_cell_colors()

    def is_inside(self, row, column):
        return 0 <= row < self.num_rows and 0 <= column < self.num_cols

    def is_empty(self, row, column):
        return self.grid[row][column] == 0

    def is_row_full(self, row):
        return all(self.grid[row])

    def clear_row(self, row):
        self.grid.pop(row)
        self.grid.insert(0, [0] * self.num_cols)

    def clear_full_rows(self):
        rows_cleared = 0
        for row in range(self.num_rows):
            if self.is_row_full(row):
                self.clear_row(row)
                rows_cleared += 1
        return rows_cleared

    def draw(self, screen, offset_x, offset_y):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.grid[row][col] != 0:
                    color = self.colors[self.grid[row][col]]
                    pygame.draw.rect(screen, color, (offset_x + col * self.cell_size, offset_y + row * self.cell_size, self.cell_size, self.cell_size))


# Class for the Tetris game
class Game:
    def __init__(self):
        self.grid1 = Grid(20, 10, 30)  # Grid for player 1
        self.grid2 = Grid(20, 10, 30)  # Grid for player 2
        self.current_block1 = self.get_random_block()
        self.current_block2 = self.get_random_block()
        self.next_block1 = self.get_random_block()
        self.next_block2 = self.get_random_block()
        self.game_over = False
        self.score1 = 0
        self.score2 = 0
        self.rotate_sound = pygame.mixer.Sound("Sounds/rotate.ogg")
        self.clear_sound = pygame.mixer.Sound("Sounds/clear.ogg")
        pygame.mixer.music.load("Sounds/music.ogg")
        pygame.mixer.music.play(-1)

    def get_random_block(self):
        blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        return random.choice(blocks)

    def move_left(self, grid):
        grid.current_block.move(0, -1)
        if not self.block_inside(grid) or not self.block_fits(grid):
            grid.current_block.move(0, 1)

    def move_right(self, grid):
        grid.current_block.move(0, 1)
        if not self.block_inside(grid) or not self.block_fits(grid):
            grid.current_block.move(0, -1)

    def move_down(self, grid):
        grid.current_block.move(1, 0)
        if not self.block_inside(grid) or not self.block_fits(grid):
            grid.current_block.move(-1, 0)
            self.lock_block(grid)

    def lock_block(self, grid):
        tiles = grid.current_block.get_cell_positions()
        for position in tiles:
            grid.grid[position.row][position.column] = grid.current_block.id
        grid.current_block = grid.next_block
        grid.next_block = self.get_random_block()
        rows_cleared = grid.clear_full_rows()
        if rows_cleared > 0:
            self.clear_sound.play()
            self.update_score(rows_cleared, 0)
        if not self.block_fits(grid):
            self.game_over = True

    def block_fits(self, grid):
        tiles = grid.current_block.get_cell_positions()
        for tile in tiles:
            if not grid.is_inside(tile.row, tile.column) or not grid.is_empty(tile.row, tile.column):
                return False
        return True

    def rotate(self, grid):
        grid.current_block.rotate()
        if not self.block_inside(grid) or not self.block_fits(grid):
            grid.current_block.undo_rotation()
        else:
            self.rotate_sound.play()

    def block_inside(self, grid):
        tiles = grid.current_block.get_cell_positions()
        for tile in tiles:
            if not grid.is_inside(tile.row, tile.column):
                return False
        return True

    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score1 += 100
            self.score2 += 100
        elif lines_cleared == 2:
            self.score1 += 300
            self.score2 += 300
        elif lines_cleared == 3:
            self.score1 += 500
            self.score2 += 500
        self.score1 += move_down_points
        self.score2 += move_down_points

    def reset(self):
        self.grid1 = Grid(20, 10, 30)
        self.grid2 = Grid(20, 10, 30)
        self.current_block1 = self.get_random_block()
        self.current_block2 = self.get_random_block()
        self.next_block1 = self.get_random_block()
        self.next_block2 = self.get_random_block()
        self.score1 = 0
        self.score2 = 0
        self.game_over = False

    def draw(self, screen):
        self.grid1.draw(screen, 20, 20)
        self.grid2.draw(screen, 260, 20)
        self.current_block1.draw(screen, 20, 20)
        self.current_block2.draw(screen, 260, 20)

        pygame.draw.rect(screen, Colors.light_blue, (170, 20, 5, 600))
        pygame.draw.rect(screen, Colors.light_blue, (170, 20, 100, 600))

        score_font = pygame.font.Font(None, 36)
        score_surface1 = score_font.render("Score: " + str(self.score1), True, Colors.white)
        score_surface2 = score_font.render("Score: " + str(self.score2), True, Colors.white)
        screen.blit(score_surface1, (20, 0))
        screen.blit(score_surface2, (260, 0))

        pygame.display.update()


# Blocks classes (same as before)
from block import Block
from position import Position

class LBlock(Block):
    """A class representing an L-shaped block in a grid-based game.

    Inherits from Block class.

    Attributes:
        Inherits all attributes from the Block class.
    
    Methods:
        Inherits all methods from the Block class.
    """

    def __init__(self):
        """Initialize an LBlock object."""
        super().__init__(id=1)
        self.cells = {
            0: [Position(0, 2), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(1, 1), Position(2, 1), Position(2, 2)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 0)],
            3: [Position(0, 0), Position(0, 1), Position(1, 1), Position(2, 1)]
        }
        self.move(0, 3)

class JBlock(Block):
    """A class representing an J-shaped block in a grid-based game.

    Inherits from Block class.

    Attributes:
        Inherits all attributes from the Block class.
    
    Methods:
        Inherits all methods from the Block class.
    """

    def __init__(self):
        super().__init__(id = 2)
        self.cells = {
            0: [Position(0, 0), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(0, 2), Position(1, 1), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 2)],
            3: [Position(0, 1), Position(1, 1), Position(2, 0), Position(2, 1)]
        }
        self.move(0, 3)

class IBlock(Block):
    """A class representing an I-shaped block in a grid-based game.

    Inherits from Block class.

    Attributes:
        Inherits all attributes from the Block class.
    
    Methods:
        Inherits all methods from the Block class.
    """

    def __init__(self):
        super().__init__(id = 3)
        self.cells = {
            0: [Position(1, 0), Position(1, 1), Position(1, 2), Position(1, 3)],
            1: [Position(0, 2), Position(1, 2), Position(2, 2), Position(3, 2)],
            2: [Position(2, 0), Position(2, 1), Position(2, 2), Position(2, 3)],
            3: [Position(0, 1), Position(1, 1), Position(2, 1), Position(3, 1)]
        }
        self.move(-1, 3)

class OBlock(Block):
    """A class representing an O-shaped block in a grid-based game.

    Inherits from Block class.

    Attributes:
        Inherits all attributes from the Block class.
    
    Methods:
        Inherits all methods from the Block class.
    """

    def __init__(self):
        super().__init__(id = 4)
        self.cells = {
            0: [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1)]
        }
        self.move(0, 4)

class SBlock(Block):
    """A class representing an S-shaped block in a grid-based game.

    Inherits from Block class.

    Attributes:
        Inherits all attributes from the Block class.
    
    Methods:
        Inherits all methods from the Block class.
    """

    def __init__(self):
        super().__init__(id = 5)
        self.cells = {
            0: [Position(0, 1), Position(0, 2), Position(1, 0), Position(1, 1)],
            1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 2)],
            2: [Position(1, 1), Position(1, 2), Position(2, 0), Position(2, 1)],
            3: [Position(0, 0), Position(1, 0), Position(1, 1), Position(2, 1)]
        }
        self.move(0, 3)

class TBlock(Block):
    """A class representing an T-shaped block in a grid-based game.

    Inherits from Block class.

    Attributes:
        Inherits all attributes from the Block class.
    
    Methods:
        Inherits all methods from the Block class.
    """

    def __init__(self):
        super().__init__(id = 6)
        self.cells = {
            0: [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1)],
            3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 1)]
        }
        self.move(0, 3)

class ZBlock(Block):
    """A class representing an Z-shaped block in a grid-based game.

    Inherits from Block class.

    Attributes:
        Inherits all attributes from the Block class.
    
    Methods:
        Inherits all methods from the Block class.
    """

    def __init__(self):
        super().__init__(id = 7)
        self.cells = {
            0: [Position(0, 0), Position(0, 1), Position(1, 1), Position(1, 2)],
            1: [Position(0, 2), Position(1, 1), Position(1, 2), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(2, 1), Position(2, 2)],
            3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 0)]
        }
        self.move(0, 3)
# Main function
def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 640))
    pygame.display.set_caption("Tetris Duel")
    clock = pygame.time.Clock()

    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and not game.game_over:
                if event.key == pygame.K_LEFT:
                    game.move_left(game.grid1)
                elif event.key == pygame.K_RIGHT:
                    game.move_right(game.grid1)
                elif event.key == pygame.K_DOWN:
                    game.move_down(game.grid1)
                elif event.key == pygame.K_UP:
                    game.rotate(game.grid1)

        if not game.game_over:
            game.draw(screen)
            clock.tick(10)

        pygame.display.flip()

if __name__ == "__main__":
    main()
