from .terminal import Terminal, EventType


class MenuScene(object):

    RETURN_VALUE_SHOW_MENU = '!showmenu!'

    str_deselected = "  {:^12}  "
    # str_selected = " - {} - "
    str_selected = "  {:^12}  "
    fmt_title = {'fg': 'yellow'}
    fmt_deselected = {'fg': '#aaa', 'bg': '#000'}
    # fmt_selected = {'fg': '#fff'}
    fmt_selected = {'fg': '#fff', 'bg': '#333'}
    fmt_disabled = {'fg': '#555'}

    def __init__(self, title, choices, fmt={}, disabled=()):
        """Initialize the menu

        title - string contianing title text
        choices - list of strings, each being a choice
        callback - callback function taking a string (choice selected) as argument
        disabled_choices (optional) - list or tuple of ints; each int is a disabled choice
        """
        self.title = title
        self.choices = tuple(obj if isinstance(obj, Choice) else Choice(obj) for obj in choices)
        self.fmt = fmt
        if 'title' in fmt:
            self.fmt_title = fmt['title']
        if 'deselected' in fmt:
            self.fmt_deselected = fmt['deselected']
        if 'selected' in fmt:
            self.fmt_selected = fmt['selected']
        if 'disabled' in fmt:
            self.fmt_disabled = fmt['disabled']
        self.disabled = disabled

    def draw_full(self):
        self.t.clear()
        self.choices_y = (self.t.h - len(self.choices)) // 2 + bool(self.title)
        if self.title:
            self.t.print_centered((self.choices_y - 2, None), self.title, **self.fmt_title)
        for i in range(len(self.choices)):
            self.draw_choice(i, False)
        self.update_selection(self.selection)  # includes a redraw

    def update_selection(self, selection=None):
        self.draw_choice(self.selection, False)
        self.selection = selection
        self.draw_choice(self.selection, True)
        self.t.redraw()

    def draw_choice(self, n, selected):
        state = 'disabled' if n in self.disabled else 'de' * (not selected) + 'selected'
        text = (self.str_deselected, self.str_selected)[
            selected].format(self.choices[n].get_text(state))
        if n in self.disabled:
            fmt = self.fmt_disabled
        else:
            fmt = (self.fmt_deselected, self.fmt_selected)[selected]
        self.t.print_centered((self.choices_y + n, None), text, **fmt)

    def show(self, canvas, selection=0, centered=True):
        self.t = canvas
        self.selection = selection
        self.centered = centered
        loop = True
        while loop:
            self.draw_full()
            return_value = self.t.loop(self.handle_event)
            loop = return_value != -1 and not self.choices[self.selection].leave_menu_when_selected
            if callable(return_value):
                return_value = return_value(self.t)
        return return_value

    def handle_event(self, e):
        if e.type == EventType.KeyPress:
            if e.keysym in ('Up', 'w', 'Down', 's'):
                diff = -1 if e.keysym in ('Up', 'w') else 1
                new_sel = self.selection + diff
                while new_sel in self.disabled:
                    new_sel += diff
                if 0 <= new_sel < len(self.choices):
                    self.update_selection(new_sel)
            elif e.keysym in ('space', 'Return'):
                self.t.exit_loop(self.choices[self.selection].select(self.selection))
            elif e.keysym in ('Escape',):
                self.t.exit_loop(-1)
            else:
                self.choices[self.selection].handle_keypress(self, e)


class Choice(object):

    leave_menu_when_selected = True

    def __init__(self, text):
        self.text = text

    def get_text(self, state):
        return self.text

    def select(self, index):
        return index

    def handle_keypress(self, menu, e):
        pass


class SpinnerChoice(Choice):

    leave_menu_when_selected = False

    def __init__(self, choices, default, on_choice=lambda choice: None, string_function=lambda choice: str(choice)):
        self.choices = choices
        if default in choices:
            self.selection = choices.index(default)
        else:
            self.selection = 0
        self.on_choice = on_choice
        self.string_function = string_function

    def get_text(self, state):
        s = self.string_function(self.choices[self.selection])
        s += ' ' * (len(s) % 2)
        f = '< {} >' if state == 'selected' else '  {}  '
        return f.format(s)

    def select(self, index):
        return self.show_menu

    def show_menu(self, terminal):
        self.selection = MenuScene(None, [self.string_function(choice) for choice in self.choices]
                                   ).show(terminal, selection=self.selection)
        self.on_choice(self.choices[self.selection])

    def handle_keypress(self, menu, e):
        """Returns True if choice needs to be redrawn"""
        if e.keysym in ('Left', 'a', 'Right', 'd'):
            diff = -1 if e.keysym in ('Left', 'a') else 1
            new_index = self.selection + diff
            if 0 <= new_index < len(self.choices):
                self.selection = new_index
                self.on_choice(self.choices[self.selection])
                menu.draw_full()
