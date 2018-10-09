from .menu import Menu
from .text import Text
from game import Area, Item
from gamedata import areas, items
from tkinter import EventType
import saveload


HELP_TEXT = """\
WASD - move
Space - select/confirm
E - open/close inventory
Q - hide menu

Use 1, 2, 3, Z, X, and C
to select items from the
hotbar.

You can disable these
hints in SETTINGS."""


class Game(object):

    def __init__(self, gamestate={}, fps=None, do_frame=lambda: None):
        self.inventory = gamestate.get('inventory', [])
        self.hotbar = Hotbar(self.hotbar_select)
        self.hotbar.items = gamestate.get('hotbar', self.hotbar.items)
        self.fps = fps
        self.do_frame = do_frame

    def show(self, surface):
        self.surf = surface
        self.surf.clear()
        self.v_border = self.surf.t.h - 3
        self.h_border = self.surf.t.w * 2 // 3

        self.hotbar_surf = self.surf.surface((self.v_border + 1, 0),
                                             (self.surf.h - 1, self.surf.w - 1))
        self.hotbar.show(self.hotbar_surf)

        self.game_surf = self.surf.surface((0, 0), (self.v_border, self.h_border))
        self.game_surf_big = self.surf.surface((0, 0), (self.v_border, -1))
        self.main_window = MainWindow()
        self.main_window.show(self.game_surf, areas.start.START)

        self.side_surf = self.surf.surface((0, self.h_border + 1),
                                           (self.v_border, self.surf.w - 1))
        self.side_surf.styles['default']['bg'] = '#422'
        self.side_surf.styles['selected']['bg'] = '#644'
        if saveload.show_help_screen:
            self.show_on_side(Text(HELP_TEXT, 'HELP', None), False)
        else:
            self.side_content = None

        self.loop = True
        while self.loop:
            return_value = self.surf.t.loop(self.handle_event,
                                            fps=self.fps,
                                            do_frame=self.do_frame)
            if isinstance(return_value, Item):
                return_value.use(self)
                self.hotbar.update_selection()

    def handle_event(self, e):
        if e.type == EventType.KeyPress:
            keysym = e.keysym.lower()
            if keysym in ('escape', 'q'):
                if self.side_content is None:
                    self.loop = False
                    self.surf.t.exit_loop()
                else:
                    self.hide_menu()
            elif keysym in ('tab', 'e',):
                if self.side_content is None:
                    self.show_on_side(Text(" Not yet implemented :(", "INVENTORY", None), False)
                else:
                    self.hide_menu()
            elif not self.hotbar.handle_event(e):
                self.main_window.handle_event(e)

    def hotbar_select(self, slot):
        self.surf.t.exit_loop(self.hotbar.items[slot])

    def show_on_side(self, thing, *args, **kwargs):
        if isinstance(thing, Menu):
            thing.str_deselected = " {{:{}}} ".format(self.side_surf.w - 4)
            thing.str_selected = " {{:{}}} ".format(self.side_surf.w - 4)
        self.main_window.set_surface(self.game_surf)
        self.main_window.draw_full()
        self.side_content = thing
        return thing.show(self.side_surf, *args, **kwargs)

    def hide_menu(self):
        self.main_window.set_surface(self.game_surf_big)
        self.main_window.draw_full()
        self.side_content = None


class Hotbar(object):

    keys = ['1', '2', '3', 'z', 'x', 'c']

    # fmt_deselected = {'fg': '#aaa', 'bg': '#122'}
    # fmt_selected = {'fg': '#fff', 'bg': '#244'}
    fmt_deselected = {'fg': '#aaa', 'bg': '#224'}
    fmt_selected = {'fg': '#fff', 'bg': '#448'}

    def __init__(self, callback):
        """Initialize the hotbar

        callback - callback function taking an integer (slot selected) as argument
        """
        self.callback = callback
        self.items = [None] * len(self.keys)

    def draw_full(self):
        self.surf.clear()
        for i in range(len(self.keys)):
            self.draw_slot(i, i == self.selection)

    def update_selection(self, selection=None):
        if self.selection is not None:
            self.draw_slot(self.selection, False)
        self.selection = selection
        if self.selection is not None:
            self.draw_slot(self.selection, True)

    def draw_slot(self, n, selected):
        w = (self.surf.w - 2) // 3
        y = n // 3 + self.surf.h // 2 - 1
        x = (w) * (n % 3) + 1
        text = self.items[n].name if self.items[n] else '< none >'
        if len(text) > w - 6:
            text = text[:(w - 9)] + '...'
        else:
            text = text.ljust(w - 6)
        style = 'de' * (not selected) + 'selected'
        self.surf.print_at((y, x), ' [{}] {} '.format(self.keys[n].upper(), text), style=style)

    def show(self, surface, selection=None):
        self.surf = surface
        self.surf.styles['default'].update(self.fmt_deselected)
        self.surf.styles['selected'].update(self.fmt_selected)
        self.selection = selection
        self.draw_full()

    def handle_event(self, e):
        if e.type == EventType.KeyPress and e.keysym.lower() in self.keys:
            i = self.keys.index(e.keysym.lower())
            if self.items[i]:
                self.update_selection(i)
            self.callback(i)
            return True


class MainWindow(object):

    def __init__(self):
        pass

    def draw_full(self):
        offset = (  # Area point at surface's (0, 0)

            (self.area.h - self.surf.h) // 2 if self.area.h < self.surf.h else  # center on surf
            0 if self.char_pos[0] < self.surf.h // 2 else  # align up
            self.area.h - self.surf.h if self.area.h - self.char_pos[0] < self.surf.h // 2 else
            self.char_pos[0] - self.surf.h // 2,  # center on char

            (self.area.w - self.surf.w) // 2 if self.area.w < self.surf.w else  # center on surf
            0 if self.char_pos[1] < self.surf.w // 2 else  # align left
            self.area.w - self.surf.w if self.area.w - self.char_pos[1] < self.surf.w // 2 else
            self.char_pos[1] - self.surf.w // 2  # center on char

        )
        self.surf.auto_flush = False
        for y in range(self.surf.h):
            for x in range(self.surf.w):
                area_y, area_x = y + offset[0], x + offset[1]
                if (area_y, area_x) == self.char_pos:
                    # self.surf.set_char((y, x), '@', '#0ff', '#000')
                    self.surf.set_char((y, x), '@', '#0ff', self.area.get_tile_at_pos((area_y, area_x)).bg)
                elif 0 <= area_y < self.area.h and 0 <= area_x < self.area.w:
                    self.surf.set_tile((y, x), self.area.get_tile_at_pos((area_y, area_x)))
                else:
                    self.surf.set_char((y, x), ' ', None, '#222')
                    pass
        self.surf.flush_all()
        # self.surf.t.root.update_idletasks()
        self.surf.auto_flush = True

    def show(self, surface, area):
        self.set_surface(surface)
        self.set_area(area)
        self.draw_full()

    def set_surface(self, surface):
        self.surf = surface

    def set_area(self, area):
        self.area = area
        self.char_pos = area.start

    def handle_event(self, e):
        if e.type == EventType.KeyPress:
            keysym = e.keysym.lower()
            if keysym in ('up', 'w', 'left', 'a', 'down', 's', 'right', 'd'):
                x_delta = (-1 if keysym in ('left', 'a') else
                           +1 if keysym in ('right', 'd') else 0)
                y_delta = (-1 if keysym in ('up', 'w') else
                           +1 if keysym in ('down', 's') else 0)
                new_y, new_x = self.char_pos[0] + y_delta, self.char_pos[1] + x_delta
                if (0 <= new_y < self.area.h and
                    0 <= new_x < self.area.w and
                        not self.area.get_tile_at_pos((new_y, new_x)).solid):
                    self.char_pos = (self.char_pos[0] + y_delta, self.char_pos[1] + x_delta)
                    self.draw_full()
