from game import Area, Tile
from gamedata import entities, items
# from gamedata.items import Locker, PencilPouch, SecretPassage, WaterFountain
from game import get_generic_tile

TUT_01 = Area(
    name='Tutorial',
    s='''\
    ~
                         ........
                         .  :1  .
                         .      .
    ......................      ......................
      $$$$$$$$  $$$$$$$$          $$$$$$$$  $$$$$$$$


                                           =
      $$$$$$$$  $$$$$$$$          $$$$$$$$  $$$&$$$$
    ......................      ......................
                         .      .
                         .  :2  .
                         ........

                                                     ~
    ''', start=(7, 4),
    tiles={
        '$': get_generic_tile('|', True)
        # '$':
    },
    entities={
        ':1': entities.WaterFountain(),
        ':2': entities.WaterFountain(),
        '&': entities.SecretPassage(),
        '=': items.PencilPouch().dropped_entity(),
    }
)
