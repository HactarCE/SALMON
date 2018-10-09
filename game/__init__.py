# Import game.Tile first, because it's required by gamedata.tiles, which is required by game.Area
from .tile import Tile

from .area import Area
from .entity import Entity
from .item import Item
