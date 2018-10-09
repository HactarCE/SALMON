from time import time
from tkinter import Tk, TclError, Text, EventType
from tkinter import NORMAL, DISABLED, END
from tkinter import font as tkFont
from traceback import print_exc
import numpy as np
import sys

PRINT_TKINTER_ERRORS = False

if __name__ == '__main__':
    from surface import Surface
else:
    from .surface import Surface


class Terminal(object):
    """Displays a Tkinter window resembling a terminal

    All indices are tuples (y, x) or (row, column). Negative coordinates work.

    Use process_events() in a loop when nothing else is happening.
    Use redraw() to update the screen. There is no guarantee that the screen will
    not be redrawn at other time, but this method is necessary to explicitly
    redraw the screen.

    set_char(), set_fg(), and set_bg() can be used to write to the screen.
    get_char(), get_fg(), and get_bg() can be used to read from the screen.
    print_at() can be used to write large amounts of text at once.
    clear() sets all fg to 'white', bg to 'black', and char to ' '.

    char_buffer, fg_buffer, and bg_buffer are Numpy arrays; modify these at will.

    event_handler is a lambda receiving one argument: event. It is called when
    any mouse or key event happens.

    do_frame is a lambda receiving no arguments. If fps is nonzero, do_frame is
    called fps times per second.

    fps is a number specifying how often to call do_frame.

    root is the Tkinter window.

    Set event_handler to whatever you want.

    Make your own main loop.
    """

    # Set fps to a nonzero value to execute do_frame fps times per second
    fps = 0
    # fps = 5

    def __init__(self, title=None, dim=(24, 80),
                 event_handler=lambda e: None,
                 fg='white', bg='black'):

        self.h, self.w = self.dim = dim
        # dtype='<U1' means strings of length 0 or 1
        self.char_buffer = np.full(self.dim, ' ', dtype='<U1')
        # dtype=object means the strings can be of any length
        self.fg_buffer = np.full(self.dim, fg, dtype=object)
        self.bg_buffer = np.full(self.dim, bg, dtype=object)
        self.tags = []

        self.root = Tk()

        if title:
            self.root.title(title)

        self.root.protocol('WM_DELETE_WINDOW', self.quit)

        self.font = tkFont.nametofont('TkFixedFont')
        self.text_widget = Text(self.root, font=self.font, padx=-1, pady=-1,
                                bg=bg, fg=fg, cursor='arrow', bd=0)

        self.event_handler = event_handler
        real_event_handler = lambda e: self.event_handler(e)
        self.text_widget.bind("<Button-1>", real_event_handler)
        self.text_widget.bind("<B1-Motion>", real_event_handler)
        self.text_widget.bind("<ButtonRelease-1>", real_event_handler)
        self.text_widget.bind("<Double-Button-1>", real_event_handler)
        self.text_widget.bind("<Enter>", real_event_handler)
        self.text_widget.bind("<Leave>", real_event_handler)
        self.text_widget.bind("<FocusIn>", real_event_handler)
        self.text_widget.bind("<FocusOut>", real_event_handler)
        self.text_widget.bind("<Key>", real_event_handler)
        self.text_widget.bind("<KeyRelease>", real_event_handler)
        self.text_widget.bind("<Shift-Up>", real_event_handler)
        self.text_widget['state'] = DISABLED

        self.text_widget.pack()
        self.set_font_size(self.get_font_size())

        self.destroyed = False

        try:
            self.flush_all()
        except TclError:
            if PRINT_TKINTER_ERRORS:
                print_exc()
            sys.exit()

    def surface(*args, **kwargs):
        return Surface(*args, **kwargs)

    def get_fixed_fonts(self):
        if not hasattr(self, 'fixed_fonts'):
            self.fixed_fonts = [tkFont.Font(family=f) for f in tkFont.families() if
                                f.lower() != 'ithkuil' and  # fuck Ithkuil
                                (not f.startswith('@')) and
                                tkFont.Font(family=f).metrics()['fixed']]
        return self.fixed_fonts

    def get_font(self):
        return self.font

    def get_font_size(self):
        return self.font['size']

    def set_font(self, font, font_size=None):
        if font_size is None:
            font_size = self.get_font_size()
        self.font = font if isinstance(font, tkFont.Font) else tkFont.Font(family=font)
        self.text_widget['font'] = self.font
        self.set_font_size(font_size)

    def set_font_size(self, size):
        self.font['size'] = size
        w = self.font.measure('0') * self.w
        h = self.font.metrics('linespace') * self.h
        self.root.geometry('{}x{}'.format(w, h))
        self.root.resizable(width=False, height=False)
        self.root.eval('tk::PlaceWindow %s center' % self.root.winfo_toplevel())
        self.text_widget.focus_set()

    def update(self):
        """Respond to window events and stuff."""
        try:
            self.root.update()
        except TclError:
            if PRINT_TKINTER_ERRORS:
                print_exc()
            sys.exit()

    def loop(self, event_handler, fps=None, do_frame=lambda: None):
        """A basic mainloop

        event_handler - function taking one argument: event
        fps (optional) - number of times to execute do_frame
        do_frame (optional) - thing to be executed fps times per second

        event_handler is called for any mouse or key event only within the loop;
        event_handler is not called for any events after the loop exits.

        fps and do_frame can both be modified from within the loop using
        term.fps or term.do_frame.

        Call exit_loop() to exit the loop. Any argument passed to exit_loop()
        will be returned by main_loop(), which can be used to retrieve
        information about what to do after the loop exits.

        DO NOT START A LOOP FROM WITHIN EVENT_HANDLER UNLESS YOU REALLY LIKE RECURSION.
        """
        self.event_handler = event_handler
        self.fps = fps
        self.do_frame = do_frame
        self.continue_loop = True
        next_frame = time()
        while self.continue_loop:
            if fps and time() >= next_frame:
                next_frame += (1 / fps)
                self.do_frame()
            if self.destroyed:
                sys.exit()
            else:
                self.update()
        self.event_handler = lambda e: None
        return self.return_value

    def exit_loop(self, return_value=None):
        self.continue_loop = False
        self.return_value = return_value

    def enable_write(self):
        self.text_widget['state'] = NORMAL

    def disable_write(self):
        self.text_widget['state'] = DISABLED

    def flush_all(self):
        """Flush everything to the text widget."""
        self.enable_write()
        self.text_widget.delete('1.0', END)
        text_buffer = ''
        last_tag = None
        for y in range(self.h):
            for x in range(self.w):
                pos = (y, x)
                tag = self.get_tag(self.fg_buffer[pos], self.bg_buffer[pos])
                if tag != last_tag:
                    self.text_widget.insert(END, text_buffer, (last_tag,))
                    text_buffer = self.char_buffer[pos]
                    last_tag = tag
                else:
                    text_buffer += self.char_buffer[pos]
            text_buffer += '\n'
        # [:-1] to remove trailing newline
        self.text_widget.insert(END, text_buffer[:-1], (last_tag,))
        self.disable_write()

    @staticmethod
    def widget_format(pos):
        return '{}.{}'.format(pos[0] + 1, pos[1])

    def get_tag(self, fg, bg):
        tag = '_{}_{}'.format(fg, bg)
        if tag not in self.tags:
            self.tags.append(tag)
            self.text_widget.tag_config(tag, foreground=fg, background=bg)
        return tag

    def quit(self):
        self.destroyed = True
        self.root.destroy()

    def simple_event_handler(self, exit_condition):
        """Return an event handler function which exists if exit_condition() returns True.

        exit_condition - function receiving an argument `event` and returning a boolean
        """
        return lambda e: exit_condition(e) and self.exit_loop()

    def wait_for_key_press(self):
        self.loop(self.simple_event_handler(lambda e: e.type == EventType.KeyPress))


if __name__ == '__main__':
    import random
    term = Terminal(title='Terminal Demo')
    surf = term.surface()
    while True:
        for i in range(10):
            pos = (random.randint(0, surf.h - 1), random.randint(0, surf.w - 1))
            colors = ['#000', '#00f', '#0f0', '#0ff', '#f00', '#f0f', '#ff0', '#fff']
            random.shuffle(colors)
            surf.set_char(pos, random.choice('abcdefghijklmnopqrstuvwxyz0123456789'),
                          fg=colors[0], bg=colors[1])
        # term.flush_all()
        surf.t.update()
