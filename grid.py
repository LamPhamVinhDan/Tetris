import pygame
from colors import Colors

class Grid:
    """A class representing the game grid.

    This class manages the grid where blocks are placed during the game.

    Attributes:
        num_rows (int): The number of rows in the grid.
        num_cols (int): The number of columns in the grid.
        cell_size (int): The size of each cell in pixels.
        grid (list): A 2D list representing the grid cells.
        colors (list): A list of colors for different cell values.

    Methods:
        print_grid(): Print the current state of the grid to the console.
        is_inside(row, column): Check if a given row and column index is inside the grid boundaries.
        is_empty(row, column): Check if a cell at a given row and column index is empty.
        is_row_full(row): Check if a given row is full (contains no empty cells).
        clear_row(row): Clear all cells in a given row.
        move_row_down(row, num_rows): Move all cells in a row down by a given number of rows.
        clear_full_rows(): Clear all full rows in the grid and move cells above down.
        reset(): Reset the grid to its initial state with all cells empty.
        draw(screen): Draw the grid on the provided Pygame screen.

    """

    def __init__(self):
        """Initialize a Grid object."""
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
        self.colors = Colors.get_cell_colors()

    def print_grid(self):
        """Print the current state of the grid to the console."""
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                print(self.grid[row][column], end=" ")
            print()

    def is_inside(self, row, column):
        """Check if a given row and column index is inside the grid boundaries.

        Args:
            row (int): The row index.
            column (int): The column index.

        Returns:
            bool: True if the index is inside the grid boundaries, False otherwise.
        """
        if 0 <= row < self.num_rows and 0 <= column < self.num_cols:
            return True
        return False

    def is_empty(self, row, column):
        """Check if a cell at a given row and column index is empty.

        Args:
            row (int): The row index.
            column (int): The column index.

        Returns:
            bool: True if the cell is empty, False otherwise.
        """
        return self.grid[row][column] == 0

    def is_row_full(self, row):
        """Check if a given row is full (contains no empty cells).

        Args:
            row (int): The row index.

        Returns:
            bool: True if the row is full, False otherwise.
        """
        return all(cell != 0 for cell in self.grid[row])

    def clear_row(self, row):
        """Clear all cells in a given row.

        Args:
            row (int): The row index.
        """
        self.grid[row] = [0] * self.num_cols

    def move_row_down(self, row, num_rows):
        """Move all cells in a row down by a given number of rows.

        Args:
            row (int): The row index.
            num_rows (int): The number of rows to move down.
        """
        for col in range(self.num_cols):
            self.grid[row + num_rows][col] = self.grid[row][col]
            self.grid[row][col] = 0

    def clear_full_rows(self):
        """Clear all full rows in the grid and move cells above down.

        Returns:
            int: The number of rows cleared.
        """
        completed = 0
        for row in range(self.num_rows - 1, 0, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1
            elif completed > 0:
                self.move_row_down(row, completed)
        return completed

    def reset(self):
        """Reset the grid to its initial state with all cells empty."""
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]

    def draw(self, screen):
        """Draw the grid on the provided Pygame screen.

        Args:
            screen (pygame.Surface): The Pygame surface to draw on.
        """
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                cell_value = self.grid[row][col]
                cell_rect = pygame.Rect(col * self.cell_size + 11, row * self.cell_size + 11,
                                         self.cell_size - 1, self.cell_size - 1)
                pygame.draw.rect(screen, self.colors[cell_value], cell_rect)