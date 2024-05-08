from colors import Colors
import pygame
from position import Position

class Block:
    """A class representing a block in a grid-based game.

    Attributes:
        id (int): The identifier of the block.
        cells (dict): A dictionary containing the positions of cells in different rotation states.
        cell_size (int): The size of each cell in pixels.
        row_offset (int): The offset in rows from the original position.
        column_offset (int): The offset in columns from the original position.
        rotation_state (int): The current rotation state of the block.
        colors (list): A list of colors for the cells in the block.

    Methods:
        move(rows, columns): Move the block by the specified number of rows and columns.
        get_cell_positions(): Get the positions of the cells in the current rotation state, accounting for offsets.
        rotate(): Rotate the block clockwise by 90 degrees.
        undo_rotation(): Undo the last rotation of the block.
        draw(screen, offset_x, offset_y): Draw the block on the screen with the specified offset.
    """

    def __init__(self, id):
        """Initialize a Block object.

        Args:
            id (int): The identifier of the block.
        """
        self.id = id
        self.cells = {}
        self.cell_size = 30
        self.row_offset = 0
        self.column_offset = 0
        self.rotation_state = 0
        self.colors = Colors.get_cell_colors()

    def move(self, rows, columns):
        """Move the block by the specified number of rows and columns.

        Args:
            rows (int): The number of rows to move.
            columns (int): The number of columns to move.
        """
        self.row_offset += rows
        self.column_offset += columns

    def get_cell_positions(self):
        """Get the positions of the cells in the current rotation state, accounting for offsets.

        Returns:
            list: A list of Position objects representing the cell positions.
        """
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for position in tiles:
            position = Position(position.row + self.row_offset, position.column + self.column_offset)
            moved_tiles.append(position)
        return moved_tiles

    def rotate(self):
        """Rotate the block clockwise by 90 degrees."""
        self.rotation_state += 1
        if self.rotation_state == len(self.cells):
            self.rotation_state = 0

    def undo_rotation(self):
        """Undo the last rotation of the block."""
        self.rotation_state -= 1
        if self.rotation_state == -1:
            self.rotation_state = len(self.cells) - 1

    def draw(self, screen, offset_x, offset_y):
        """Draw the block on the screen with the specified offset.

        Args:
            screen: The Pygame screen surface to draw on.
            offset_x (int): The x-coordinate offset.
            offset_y (int): The y-coordinate offset.
        """
        tiles = self.get_cell_positions()
        for tile in tiles:
            tile_rect = pygame.Rect(offset_x + tile.column * self.cell_size, 
                offset_y + tile.row * self.cell_size, self.cell_size -1, self.cell_size -1)
            pygame.draw.rect(screen, self.colors[self.id], tile_rect)