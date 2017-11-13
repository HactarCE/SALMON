from tkinter import EventType


class Text(object):

    def __init__(self, text, title=None, caption='Press [Enter] to continue...'):
        """Initialize the menu

        title - string contianing title text
        choices - list of strings, each being a choice
        callback - callback function taking a string (choice selected) as argument
        disabled_choices (optional) - list or tuple of ints; each int is a disabled choice
        """
        self.text = text
        self.title = title
        self.caption = caption

    def draw_full(self):
        self.surf.clear()
        if self.title:
            self.surf.print_at((1, 1), self.title, 'title')
        self.surf.print_at((3, 1), self.text, 'content')
        if self.caption:
            self.surf.print_at((-2, 1), self.caption, 'caption')

    def show(self, surface, loop=True):
        self.surf = surface
        self.draw_full()
        if loop:
            self.surf.t.loop(self.handle_event)

    def handle_event(self, e):
        if e.type == EventType.KeyPress:
            if e.keysym.lower() in ('space', 'return', 'escape', 'q'):
                self.surf.t.exit_loop()
