from .terminal import Terminal, EventType
import textwrap


class ExpositionScene(object):

    fmt_title = {'fg': 'yellow'}
    fmt_text = {'fg': '#ddd'}
    fmt_caption = {'fg': '#aaa'}

    def __init__(self, text, title='', caption='Press [Enter] to continue…...'):
        """Initialize the menu

        title - string contianing title text
        choices - list of strings, each being a choice
        callback - callback function taking a string (choice selected) as argument
        disabled_choices (optional) - list or tuple of ints; each int is a disabled choice
        """
        self.text = '\n'.join(textwrap.fill(s) for s in text.splitlines())
        self.title = title
        self.caption = caption

    def draw_full(self):
        self.t.clear()
        # title_lines = self.title.splitlines()
        # y = (self.t.h - len(self.choices) - len(title_lines) - 1) // 2
        # for line in title_lines:
        #     self.t.print_centered((y, None), line, **self.fmt_title)
        #     y += 1
        self.t.print_centered((1, None), self.title, **self.fmt_title)
        self.t.print_centered(None, self.text, **self.fmt_text)
        self.t.print_centered((-2, None), self.caption, **self.fmt_caption)
        self.t.redraw()

    def show(self, terminal):
        self.t = terminal
        self.draw_full()
        self.t.loop(self.handle_event)

    def handle_event(self, e):
        if e.type == EventType.KeyPress:
            if e.keysym in ('space', 'Return'):
                self.t.exit_loop()
