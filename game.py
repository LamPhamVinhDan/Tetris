from grid import Grid
from blocks import *
import random
import pygame

class Game:
    """A class representing the main game logic and state.

    This class manages the game grid, blocks, player's score, and game state.

    Attributes:
        grid (Grid): The game grid where blocks are placed.
        blocks (list): A list of available blocks for the game.
        current_block (Block): The currently active block in the game.
        next_block (Block): The next block to appear in the game.
        game_over (bool): A flag indicating whether the game is over.
        score (int): The player's current score in the game.
        rotate_sound (pygame.mixer.Sound): The sound effect for block rotation.
        clear_sound (pygame.mixer.Sound): The sound effect for clearing lines.

    Methods:
        update_score(lines_cleared, move_down_points): Update the player's score based on cleared lines and move points.
        get_random_block(): Get a random block from the available blocks.
        move_left(): Move the current block to the left if possible.
        move_right(): Move the current block to the right if possible.
        move_down(): Move the current block down if possible.
        lock_block(): Lock the current block in place on the grid.
        reset(): Reset the game to its initial state.
        block_fits(): Check if the current block fits within the grid boundaries.
        rotate(): Rotate the current block if possible.
        block_inside(): Check if the current block is inside the grid boundaries.
        draw(screen): Draw the game elements on the provided Pygame screen.

    """

    def __init__(self):
        """Initialize a Game object."""
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.rotate_sound = pygame.mixer.Sound("Sounds/rotate.ogg")
        self.clear_sound = pygame.mixer.Sound("Sounds/clear.ogg")

        pygame.mixer.music.load("Sounds/music.ogg")
        pygame.mixer.music.play(-1)

    def update_score(self, lines_cleared, move_down_points):
        """Update the player's score based on cleared lines and move points.

        Args:
            lines_cleared (int): The number of lines cleared in a single move.
            move_down_points (int): The points earned from moving the block down.
        """
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        self.score += move_down_points

    def get_random_block(self):
        """Get a random block from the available blocks.

        Returns:
            Block: A randomly selected block object.
        """
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def move_left(self):
        """Move the current block to the left if possible."""
        self.current_block.move(0, -1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, 1)

    def move_right(self):
        """Move the current block to the right if possible."""
        self.current_block.move(0, 1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, -1)

    def move_down(self):
        """Move the current block down if possible."""
        self.current_block.move(1, 0)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(-1, 0)
            self.lock_block()

    def lock_block(self):
        """Lock the current block in place on the grid."""
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        if rows_cleared > 0:
            self.clear_sound.play()
            self.update_score(rows_cleared, 0)
        if not self.block_fits():
            self.game_over = True

    def reset(self):
        """Reset the game to its initial state."""
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0
        self.game_over = False

    def block_fits(self):
        """Check if the current block fits within the grid boundaries."""
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_empty(tile.row, tile.column):
                return False
        return True

    def rotate(self):
        """Rotate the current block if possible."""
        self.current_block.rotate()
        if not self.block_inside() or not self.block_fits():
            self.current_block.undo_rotation()
        else:
            self.rotate_sound.play()

    def block_inside(self):
        """Check if the current block is inside the grid boundaries."""
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_inside(tile.row, tile.column):
                return False
        return True

    def draw(self, screen):
        """Draw the game elements on the provided Pygame screen."""
        self.grid.draw(screen)
        self.current_block.draw(screen, 11, 11)

        if self.next_block.id == 3:
            self.next_block.draw(screen, 255, 290)
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 255, 280)
        else:
            self.next_block.draw(screen, 270, 270)