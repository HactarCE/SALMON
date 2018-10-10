from game import Tile, get_generic_tile

TILES = {
    None: Tile(' ', None, '#000'),
    ' ': Tile(' ', None, '#000'),
    '.': get_generic_tile(' ', True),
    '|': get_generic_tile('|', True),
    ':': get_generic_tile(':', True),
    # ' ': Tile(' ', '#fff', '#000'),
    # '~': Tile('~', '#fff', '#000'),
    '#': Tile('#', '#fff', '#050', True),
}
