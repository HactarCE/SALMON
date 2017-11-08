from time import time
from tkinter import *
from tkinter.font import nametofont
from traceback import print_exc
import numpy as np


class Terminal(object):
    """Displays a Tkinter window resembling a term

    All indices are tuples (y, x) or (row, column). Negative coordinates work.

    Use idle() in a loop when nothing else is happening.
    Use update() to update the screen.

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
    # fps = 30

    def __init__(self, title=None, dim=(24, 80), event_handler=lambda e: None, fg='white', bg='black'):

        self.h, self.w = self.dim = dim
        self.clear(' ', fg, bg)
        self.tags = []

        self.root = Tk()

        if title:
            self.root.title(title)

        self.root.protocol('WM_DELETE_WINDOW', self.quit)

        self.font = nametofont('TkFixedFont')
        self.text_widget = Text(self.root, font=self.font, padx=-1, pady=-1,
                                bg=bg, fg=fg)

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

        self.redraw()

    def get_font_size(self):
        return self.font['size']

    def set_font_size(self, size):
        self.font['size'] = size
        w = self.font.measure('0') * self.w
        h = self.font.metrics('linespace') * self.h
        self.root.geometry('{}x{}'.format(w, h))
        self.root.resizable(width=False, height=False)
        self.root.eval('tk::PlaceWindow %s center' % self.root.winfo_toplevel())
        self.text_widget.focus_set()

    def loop(self, event_handler, fps=None, do_frame=lambda: None):
        """A basic mainloop

        event_handler - function taking one argument: event
        fps (optional) - number of times to execute do_frame
        do_frame (optional) - thing to be executed fps times per second

        event_handler is called for any mouse or key event only within the loop;
        event_handler is not called for any events after the loop exits.

        fps and do_frame can both be modified from within the loop using
        term.fps or term.do_frame.

        Call redraw() yourself.

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
            self.process_events()
        self.event_handler = lambda e: None
        return self.return_value

    def exit_loop(self, return_value=None):
        self.continue_loop = False
        self.return_value = return_value

    def clear(self, char=' ', fg='white', bg='black'):
        """Clear the buffer"""
        self.char_buffer = np.full(
            self.dim, ' ')  # dtype will be <U1 because all strings are the same length
        # dtype=object means the strings can be of any length
        self.fg_buffer = np.full(self.dim, fg, dtype=object)
        self.bg_buffer = np.full(self.dim, bg, dtype=object)

    def process_events(self):
        """Respond to window events and stuff"""
        try:
            self.root.update()
        except TclError:
            print_exc()
            sys.exit()

    def redraw(self):
        """Update the screen visually"""
        try:
            self.refresh()  # load buffer into text widget
            self.root.update_idletasks()
        except TclError:
            print_exc()
            sys.exit()

    def refresh_cell(self, pos):
        self.text_widget.delete(self.widget_format(pos))
        tag = self.get_tag(pos)
        self.text_widget.insert(self.widget_format(pos), self.get_char(pos), tag)
        self.config_tag(tag)

    def get_char(self, pos):
        return self.char_buffer[pos]

    def get_fg(self, pos):
        return self.fg_buffer[pos]

    def get_bg(self, pos):
        return self.bg_buffer[pos]

    def set_char(self, pos, char, fg=None, bg=None):
        self.char_buffer[pos] = char
        if fg:
            self.set_fg(pos, fg)
        if bg:
            self.set_bg(pos, bg)

    def set_fg(self, pos, color):
        self.fg_buffer[pos] = color

    def set_bg(self, pos, color):
        self.bg_buffer[pos] = color

    def print_at(self, pos, chars, fg=None, bg=None):
        y, x = pos
        for line in chars.splitlines():
            end_x = x + len(line)
            self.char_buffer[y][x:end_x] = list(line)
            if fg:
                self.fg_buffer[y][x:end_x] = fg
            if bg:
                self.bg_buffer[y][x:end_x] = bg
            # for i in range(x, end_x):
                # self.refresh_cell((y, i))
            y += 1

    def refresh(self):
        """Flush everything to the text widget"""
        self.text_widget['state'] = NORMAL
        self.text_widget.delete('1.0', END)
        text_buffer = ''
        last_tag = None
        for y in range(self.h):
            for x in range(self.w):
                pos = (y, x)
                tag = self.get_tag(pos)
                if tag != last_tag:
                    self.text_widget.insert(END, text_buffer, (last_tag,))
                    self.config_tag(tag)
                    text_buffer = self.get_char(pos)
                    last_tag = tag
                else:
                    text_buffer += self.get_char(pos)
            text_buffer += '\n'
        # [:-1] to remove trailing newline
        self.text_widget.insert(END, text_buffer[:-1], (last_tag,))
        self.config_tag(tag)
        self.text_widget['state'] = DISABLED

    def widget_format(self, pos):
        return '{}.{}'.format(pos[0] + 1, pos[1])

    def get_tag(self, pos):
        return '_{}_{}'.format(self.get_fg(pos), self.get_bg(pos))

    def config_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)
            _, fg, bg = tag.split('_')
            self.text_widget.tag_config(tag, foreground=fg, background=bg)

    def add_pos(self, pos1, pos2):
        return (pos1[0] + pos2[0], pos1[1] + pos2[1])

    def quit(self):
        self.root.destroy()

    def print_centered(self, pos, text, fg=None, bg=None):
        """Prints text centered at pos

        pos=None --> horizontally and vertically centered on screwen
        pos=(y, None) --> horizontally centered on screen at Y
        pos=(None, x) --> vertically centered on screen at X
        pos=(y, x) --> centered at (Y, X)

        Multiline text is ok.
        """
        lines = text.splitlines()
        y, x = pos if pos else (None, None)
        y = int((self.h / 2 - 0.5 if y is None else y) - len(lines) / 2 + 0.5)
        mid_x = self.w / 2 if x is None else x
        for line in lines:
            x = int(mid_x - len(line) / 2)
            self.print_at((y, x), line, fg=fg, bg=bg)
            y += 1

    def simple_event_handler(self, exit_condition):
        """Returns an event handler function which exists if exit_condition() returns True

        exit_condition - function receiving an argument `event` and returning a boolean
        """
        return lambda e: exit_condition(e) and self.exit_loop()

    def wait_for_key_press(self):
        self.loop(self.simple_event_handler(lambda e: e.type == EventType.KeyPress))

if __name__ == '__main__':
    import random
    term = Terminal(title='SALMON')
    while True:
        for i in range(10):
            pos = (random.randint(0, term.rows - 1), random.randint(0, term.columns - 1))
            colors = ['#000', '#00f', '#0f0', '#0ff', '#f00', '#f0f', '#ff0', '#fff']
            random.shuffle(colors)
            term.set_char(pos, random.choice('abcdefghijklmnopqrstuvwxyz'),
                             fg=colors[0], bg=colors[1])
        term.redraw()
