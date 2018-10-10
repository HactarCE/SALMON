from game import Entity, Tile, get_generic_tile
import numpy as np

class Item(object):

    name = "Generic item"
    dropped_tile = Tile('?', '#fff', '#f0f')

    def use(self, game):
        pass

    def dropped_entity(self):
        return DroppedItem(self)


class DroppedItem(Entity):

    def __init__(self, item):
        self.item = item
        self.tile_array = np.array([[item.dropped_tile]])
