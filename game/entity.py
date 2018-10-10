from game import Tile, get_generic_tile
import numpy as np


class Entity(object):

    def __init__(self):
        self.tile_array = np.array([[Tile('?', '#fff', '#f00', True)]])

    def init(self, area, pos):
        """Notify the entity of its area and position in that area.

        pos should be in the form (y, x)

        This method should be called when the area is first loaded, and whenever
        the entity moves to a different area.
        """
        self.area = area
        self.pos = pos

    def interact(self, game, relative_pos):
        pass
