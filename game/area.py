from collections import defaultdict
from gamedata.tiles import TILES, get_generic_tile
from textwrap import dedent
import numpy as np


class Area(object):
    """A game area consisting of tiles, entities, and items.

    name - The name of the area.
    s - A string representing the positions of tiles.
    start - A tuple (y, x) representing
    """

    def __init__(self, name, s, start=(0, 0), tiles={}, obj={}, items={}):
        self.name = name
        self.s = dedent(s).strip().replace('~', ' ')
        self.start = start
        self.tiles = {**TILES, **tiles}
        self.objects = obj
        self.items = items

        self.lines = self.s.splitlines()
        self.h = len(self.lines)
        self.w = len(self.lines[-1])
        self.tile_array = np.full((self.h, self.w), self.tiles[None])
        # self.colors = np.full((self.h, self.w), '', dtype=object)
        for y, line in enumerate(self.lines):
            for x, char in enumerate(line):
                self.tile_array[y, x] = self.get_char_tile(char)

    def get_char_tile(self, char):
        if char in self.tiles:
            return self.tiles[char]
        else:
            # return self.tiles[None]
            return get_generic_tile(char)

    def get_tile_at_pos(self, pos):
        return self.tile_array[pos]
