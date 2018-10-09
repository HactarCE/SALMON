from tkinter import EventType


MIN_HIGHLIGHT_WIDTH = 16


class Menu(object):

    str_deselected_centered = f"  {{:^{MIN_HIGHLIGHT_WIDTH}}}  "
    str_selected_centered = f"  {{:^{MIN_HIGHLIGHT_WIDTH}}}  "
    str_deselected = f"  {{:{MIN_HIGHLIGHT_WIDTH}}}  "
    str_selected = f"  {{:{MIN_HIGHLIGHT_WIDTH}}}  "

    def __init__(self, title, choices, disabled_choices=(), scroll=False):
        self.title = title
        self.choices = tuple(obj if isinstance(obj, Choice) else Choice(obj) for obj in choices)
        self.disabled_choices = disabled_choices
        self.scroll = scroll

    def show(self, surface, selection=0):
        self.surf = surface
        self.selection = selection
        self.return_value = None
        self.loop = True
        # i = 0
        # for choice in self.choices:
        #     choice.menu, choice.index = self, i
        #     i += 1
        while self.loop:
            self.draw_full()
            selected_choice = self.surf.t.loop(self.handle_event)
            if selected_choice == -1:  # user pressed [Esc] to close menu
                self.close(-1)
            else:
                self.choices[selected_choice].select(self, selected_choice)
        return self.return_value

    def close(self, return_value):
        self.loop = False
        self.return_value = return_value

    def draw_full(self):
        self.surf.clear()
        if self.scroll:
            self.choices_y = self.surf.y_center - self.selection
        elif self.surf.get_style('content')['center_v']:
            self.choices_y = (self.surf.t.h - len(self.choices)) // 2 + bool(self.title)
        else:
            self.choices_y = 3
        if self.title and self.choices_y > 2:
            self.surf.print_at((self.choices_y - 2, 1), self.title, style='title')
        for i in range(len(self.choices)):
            if 0 <= self.choices_y + i < self.surf.h:
                self.draw_choice(i, False)
        self.update_selection(self.selection)

    def draw_choice(self, index, selected):
        if index in self.disabled_choices:
            state = 'disabled'
        else:
            state = 'de' * (not selected) + 'selected'
        fmt = getattr(self, 'str_' + 'de' * (not selected) + 'selected' +
                      '_centered' * bool(self.surf.get_style(state)['center_h']))
        # fmt = (self.str_deselected, self.str_selected)[selected]
        text = fmt.format(self.choices[index].get_text(state))
        self.surf.print_at((self.choices_y + index, 1), text, style=state)

    def update_selection(self, selection=None):
        self.draw_choice(self.selection, False)
        self.selection = selection
        self.draw_choice(self.selection, True)

    def handle_event(self, e):
        if e.type == EventType.KeyPress:
            keysym = e.keysym.lower()
            if keysym in ('up', 'w', 'down', 's'):
                delta = -1 if keysym in ('up', 'w') else 1
                new_sel = self.selection + delta
                while new_sel in self.disabled_choices:
                    new_sel += delta
                if 0 <= new_sel < len(self.choices):
                    if self.scroll:
                        self.selection = new_sel
                        self.draw_full()
                    else:
                        self.update_selection(new_sel)
            elif keysym in ('space', 'return'):
                self.surf.t.exit_loop(self.selection)
            elif keysym in ('escape', 'q'):
                self.surf.t.exit_loop(-1)
            else:
                self.choices[self.selection].handle_keypress(self, e)


class Choice(object):

    # # Menu will set these when necessary
    # menu = None
    # index = None

    def __init__(self, text):
        self.text = text

    def get_text(self, state):
        return self.text

    def select(self, menu, index):
        menu.close(index)

    def handle_keypress(self, menu, e):
        """Handle keypress and return True if choice needs to be redrawn."""
        return False


class SpinnerChoice(Choice):

    def __init__(self, choices, default, on_choice=lambda choice: None,
                 string_function=lambda choice: str(choice)):
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

    def select(self, menu, index):
        old_selection = self.selection
        self.selection = Menu(None, [self.string_function(choice) for choice in self.choices],
                              scroll=True).show(menu.surf, selection=self.selection)
        if self.selection == -1:
            self.selection = old_selection
        else:
            self.on_choice(self.choices[self.selection])

    def handle_keypress(self, menu, e):
        """Returns True if choice needs to be redrawn"""
        if e.keysym in ('Left', 'a', 'Right', 'd'):
            diff = -1 if e.keysym in ('Left', 'a') else +1
            self.selection = (self.selection + diff) % len(self.choices)
            self.on_choice(self.choices[self.selection])
            menu.draw_full()
