class Position:
    """A class representing a position in a grid.

    Attributes:
        row (int): The row index of the position.
        column (int): The column index of the position.

    """

    def __init__(self, row, column):
        """Initialize a Position object with the given row and column indices.

        Args:
            row (int): The row index of the position.
            column (int): The column index of the position.
        """
        self.row = row
        self.column = column