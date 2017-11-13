from game import Item
from tui import Menu


class Teleporter(Item):

    name = 'Teleporter'

    def __init__(self, destinations):
        self.areas = destinations
        self.area_names = [d.name for d in destinations]

    def use(self, game):
        selection = game.show_on_side(Menu(self.name.upper(), self.area_names))
        if selection != -1:
            game.main_window.set_area(self.areas[selection])
        game.hide_menu()
        # game.main_window.draw_full()
