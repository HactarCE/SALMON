from game import Tile

def get_generic_tile(char, solid=False):
    return Tile(char, '#fff', '#444', solid)

TILES = {
    None: Tile(' ', None, '#000'),
    ' ': Tile(' ', None, '#000'),
    '.': get_generic_tile(' '),
    '|': get_generic_tile('|', True),
    ':': get_generic_tile(':', True),
    # ' ': Tile(' ', '#fff', '#000'),
    # '~': Tile('~', '#fff', '#000'),
    '#': Tile('#', '#fff', '#050', True),
}
