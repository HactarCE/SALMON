class Tile(object):
    """A tile in an Area.

    char - The character to display.
    fg - The foreground color (default None).
    bg - The background color (default None).
    solid - Whether the tile is solid; True if the player cannot walk through it (default None).
    """

    def __init__(self, char, fg=None, bg=None, solid=False):
        self.char = char
        self.fg = fg
        self.bg = bg
        self.solid = solid
