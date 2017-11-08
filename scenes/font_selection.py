from .menu import *


class FontSizeSelectionScene(MenuScene):

    font_sizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 24]

    def __init__(self):
        super().__init__("CHANGE FONT SIZE", ['BACK', ''])

    def draw_choice(self, n, selected):
        text = (self.str_deselected, self.str_selected)[selected].format(self.choices[n])
        fmt = (self.fmt_deselected, self.fmt_selected)[selected]
        self.t.print_centered((self.choices_y + n, None), text, **fmt)
        self.t.redraw()

    def show(self, terminal):
        font_size = terminal.get_font_size()
        if font_size not in self.font_sizes:
            self.font_sizes = sorted(self.font_sizes + font_size)
        self.size_index = self.font_sizes.index(font_size)
        self.update_choice()
        super().show(terminal)

    def handle_event(self, e):
        super().handle_event(e)
        if e.type == EventType.KeyPress and self.selection == 1 and e.keysym in ('Left', 'a', 'Right', 'd'):
            diff = -1 if e.keysym in ('Left', 'a') else 1
            if 0 <= self.size_index + diff < len(self.font_sizes):
                self.size_index += diff
                self.t.set_font_size(self.font_sizes[self.size_index])
                self.update_choice()
                self.draw_choice(1, True)

    def update_choice(self):
        self.choices[1] = '< {:^2} >'.format(self.font_sizes[self.size_index])
