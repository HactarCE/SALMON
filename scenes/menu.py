from .terminal import Terminal, EventType


class MenuScene(object):

    str_deselected = "  {}  "
    str_selected = "> {} <"
    fmt_title = {'fg': 'yellow'}
    fmt_deselected = {'fg': '#aaa'}
    fmt_selected = {'fg': '#fff'}
    fmt_disabled = {'fg': '#555'}

    def __init__(self, title, choices, callback, disabled_choices=()):
        """Initialize the menu

        title - string contianing title text
        choices - list of strings, each being a choice
        callback - callback function taking a string (choice selected) as argument
        disabled_choices (optional) - list or tuple of ints; each int is a disabled choice
        """
        self.title = title
        self.choices = choices
        self.callback = callback
        self.disabled_choices = disabled_choices

    def draw_full(self):
        self.t.clear()
        title_lines = self.title.splitlines()
        y = (self.t.h - len(self.choices) - len(title_lines) - 1) // 2
        for line in title_lines:
            self.t.print_centered((y, None), line, **self.fmt_title)
            y += 1
        self.choices_y = y + 1
        for i in range(len(self.choices)):
            self.draw_choice(i, False)
        self.update_selection(self.selection) # includes a redraw

    def update_selection(self, selection=None):
        self.draw_choice(self.selection, False)
        self.selection = selection
        self.draw_choice(self.selection, True)
        self.t.redraw()

    def draw_choice(self, n, selected):
        text = (self.str_deselected, self.str_selected)[selected].format(self.choices[n])
        if n in self.disabled_choices:
            fmt = self.fmt_disabled
        else:
            fmt = (self.fmt_deselected, self.fmt_selected)[selected]
        self.t.print_centered((self.choices_y + n, None), text, **fmt)

    def show(self, terminal):
        self.t = terminal
        self.selection = 0
        self.draw_full()
        data, = self.t.loop(self.handle_event)
        if data == 'select':
            self.callback(self.selection)
        elif data == 'exit':
            self.t.quit()

    def handle_event(self, e):
        if e.type == EventType.KeyPress:
            if e.keysym in ('Up', 'w', 'Down', 's'):
                diff = -1 if e.keysym in ('Up', 'w') else 1
                new_sel = self.selection + diff
                while new_sel in self.disabled_choices:
                    new_sel += diff
                if 0 <= new_sel < len(self.choices):
                    self.update_selection(new_sel)
            elif e.keysym in ('space', 'Return'):
                self.t.exit_loop('select')
            elif e.keysym in ('Escape'):
                self.t.exit_loop('exit')
            # else:
            #     print(e)
