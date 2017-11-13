import numpy as np
from textwrap import dedent


# class Tile(object):
#     def __init__(self, char):
#         self.char = (' ' if char == '~' else
#                      char)
#


TILES = {
    # 'char': ('color', solid)
    None: ('#222', False),
    ' ': ('#000', False),
    '~': ('#000', False),
    '#': ('#050', True),
}
for c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_\'`.':
    TILES[c] = ('#444', False)


class Area(object):

    def __init__(self, name, s, start=(0, 0)):
        self.name = name
        self.s = dedent(s).strip().replace('~', ' ')
        self.start = start
        self.lines = self.s.splitlines()
        self.h = len(self.lines)
        self.w = len(self.lines[-1])
        self.tiles = np.full((self.h, self.w), ' ')
        # self.colors = np.full((self.h, self.w), '', dtype=object)
        for y, line in enumerate(self.lines):
            for x, char in enumerate(line):
                self.tiles[y, x] = char

    def get_pos(self, pos):
        char = self.tiles[pos]
        if char == '.':
            char = ' '
        return (char, '#fff', *TILES.get(self.tiles[pos], ('#444', True)))
