from collections import defaultdict
from game import get_generic_tile
from gamedata.tiles import TILES
from textwrap import dedent
import numpy as np
import utils


class Area(object):
    """A game area consisting of tiles, entities, and items.

    name - The name of the area.
    s - A string representing the positions of tiles.
    start - A tuple (y, x) representing the initial position of the player.
    tiles - A dictionary mapping characters to tiles.
    entities - A dictionary mapping character sequences to entities.
    """

    def __init__(self, name, s, start=(0, 0), tiles={}, entities={}):
        self.name = name
        self.s = dedent(s).strip().replace('~', ' ')
        self.start = start
        self.tiles = {**TILES, **tiles}

        self.entities = []
        self.lines = self.s.splitlines()
        self.h = len(self.lines)
        self.w = len(self.lines[-1])
        self.tile_array_source = np.full((self.h, self.w), self.tiles[None])
        for y, line in enumerate(self.lines):
            for entity_string, entity in entities.items():
                if entity_string in line and not entity in self.entities:
                    self.entities.append(entity)
                    entity.init(self, (y, line.find(entity_string)))
                    line = line.replace(entity_string, ' ' * len(entity_string))
            for x, char in enumerate(line):
                self.tile_array_source[y, x] = self.get_char_tile(char)
        self.update_entities()

    def get_char_tile(self, char):
        if char in self.tiles:
            return self.tiles[char]
        else:
            return get_generic_tile(char)

    def get_tile_at_pos(self, pos):
        return self.tile_array[pos]

    def update_entities(self):
        self.tile_array = np.copy(self.tile_array_source)
        for entity in self.entities:
            utils.np_blit(self.tile_array, entity.tile_array, entity.pos)
