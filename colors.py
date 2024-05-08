class Colors:
    """A class representing a collection of colors for the game blocks.

    Attributes:
        dark_grey (tuple): RGB color code for dark grey.
        green (tuple): RGB color code for green.
        red (tuple): RGB color code for red.
        orange (tuple): RGB color code for orange.
        yellow (tuple): RGB color code for yellow.
        purple (tuple): RGB color code for purple.
        cyan (tuple): RGB color code for cyan.
        blue (tuple): RGB color code for blue.
        white (tuple): RGB color code for white.
        dark_blue (tuple): RGB color code for dark blue.
        light_blue (tuple): RGB color code for light blue.

    Methods:
        get_cell_colors(): Returns a list of colors for the game cells.
    """

    dark_grey = (26, 31, 40)
    green = (47, 230, 23)
    red = (232, 18, 18)
    orange = (226, 116, 17)
    yellow = (237, 234, 4)
    purple = (166, 0, 247)
    cyan = (21, 204, 209)
    blue = (13, 64, 216)
    white = (255, 255, 255)
    dark_blue = (44, 44, 127)
    light_blue = (59, 85, 162)

    @classmethod
    def get_cell_colors(cls):
        """Get a list of colors for the game cells.

        Returns:
            list: A list of RGB color codes representing the colors for the game cells.
        """
        return [cls.dark_grey, cls.green, cls.red, cls.orange, cls.yellow, cls.purple, cls.cyan, cls.blue]