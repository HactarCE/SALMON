from copy import deepcopy
from tkinter import TclError
from traceback import print_exc
import sys
import textwrap

PRINT_TKINTER_ERRORS = False


class Surface(object):
    """A rectangular area of a Terminal that can be drawn to

    Coordinates are tuples of the form (y, x). Out-of-bounds coordinates wrap.

    STYLE PARAMETERS
    fg (string) - foreground color
    bg (string) - background color
    center_h (int) - horizontal centering
        center_h = 0 - do not center horizontally
        center_h = 1 - center horizontally at X coordinate
        center_h = 2 - ignore X coordinate and center horizontally to surface
    center_v (int) - vertical centering
        center_v = 0 - do not center vertically
        center_v = 1 - center vertically at Y coordinate
        center_v = 2 - ignore Y coordinate and center vertically to surface
    wrap (bool) - wrap text (preserves newlines)
    """

    styles = {
        'default': {
            'fg': '#aaa',
            'bg': '#000',
            'center_h': 0,
            'center_v': 0,
            'wrap': False,
            'wrap_margin': 1
        },
        'clear': {
            'char': ' ',
            'center_h': 0,
            'center_v': 0,
            'wrap': False,
            'wrap_margin': 0
        },
        'title': {
            'fg': '#ff0',
            'center_h': 2
        },
        'content': {
            'fg': '#ddd',
            'wrap': True
        },
        'caption': {
            # '_base': 'content',
            'fg': '#aaa'
        },
        'deselected': {
            # '_base': 'content',
            'fg': '#aaa'
        },
        'selected': {
            # '_base': 'content',
            'fg': '#fff',
            'bg': '#333'
        },
        'disabled': {
            # '_base': 'content',
            'fg': '#555'
        }
    }

    def __init__(self, terminal, corner1=(0, 0), corner2=(-1, -1)):
        self.t = terminal
        self.y1, self.y2 = sorted(map(lambda y: y % self.t.h, (corner1[0], corner2[0])))
        self.x1, self.x2 = sorted(map(lambda x: x % self.t.w, (corner1[1], corner2[1])))
        self.dim = (self.h, self.w) = (self.y2 - self.y1 + 1, self.x2 - self.x1 + 1)
        # self.center = (self.y_center, self.x_center) = (self.h // 2, int((self.w - 0.5) / 2))
        self.center = (self.y_center, self.x_center) = (self.h // 2, self.w // 2)
        self.styles = deepcopy(self.styles)
        # for v in self.styles.values():
        #     if '_base' in v:
        #         # TODO: does not work if more than one layer of inheritance
        #         v.update(self.styles['_base'])
        self.auto_flush = True

    def wrap_pos(self, pos):
        """Wrap position to be contained by surface."""
        if pos is None:
            pos = (None, None)
        return (self.y_center if pos[0] is None else pos[0] % self.h,
                self.x_center if pos[1] is None else pos[1] % self.w)

    def get_global_pos(self, pos):
        """Convert surface-relative position to terminal-relative."""
        pos = self.wrap_pos(pos)
        return (pos[0] + self.y1, pos[1] + self.x1)

    def surface(self, corner1=(0, 0), corner2=(-1, -1)):
        """Create a new subsurface of this surface."""
        surf = self.t.surface(self.get_global_pos(corner1), self.get_global_pos(corner2))
        # surf.styles = deepcopy(self.styles)
        return surf

    def get_style(self, style):
        """Return a copy of named style, if present, otherwise returns a copy of style."""
        if isinstance(style, str) and style in self.styles:
            style = self.styles[style]
        return {**self.styles['default'], **style}

    def get_char(self, pos):
        return self.t.char_buffer[self.get_global_pos(pos)]

    def get_fg(self, pos):
        return self.t.fg_buffer[self.get_global_pos(pos)]

    def get_bg(self, pos):
        return self.t.bg_buffer[self.get_global_pos(pos)]

    def set_char(self, pos, char=None, fg=None, bg=None):
        pos = self.get_global_pos(pos)
        if char:
            self.t.char_buffer[pos] = char
        else:
            char = self.t.char_buffer[pos]
        if fg:
            self.t.fg_buffer[pos] = fg
        else:
            fg = self.t.fg_buffer[pos]
        if bg:
            self.t.bg_buffer[pos] = bg
        else:
            bg = self.t.bg_buffer[pos]
        tag = self.t.get_tag(fg, bg)
        if self.auto_flush:
            try:
                self.t.enable_write()
                self.t.text_widget.delete(self.t.widget_format(pos))
                self.t.text_widget.insert(self.t.widget_format(pos), char, (tag,))
                self.t.disable_write()
            except TclError:
                if PRINT_TKINTER_ERRORS:
                    print_exc()
                sys.exit()

    def print_at(self, pos, text, style='default'):
        """Print text at pos."""

        style = self.get_style(style)
        fg, bg = style['fg'], style['bg']
        center_v, center_h = style['center_v'], style['center_h']

        max_lines = (
            self.h - pos[0],
            2 * min(pos[0], self.h - pos[0] - 1) + 1,
            self.h
        )[center_v]
        max_line_length = (
            self.w - pos[1],
            2 * min(pos[1], self.w - pos[1] - 1) + 1,
            self.w
        )[center_h]

        if style['wrap']:
            lines = '\n'.join(textwrap.fill(s, max_line_length - style['wrap_margin'])
                              for s in text.splitlines()).splitlines()
        else:
            lines = [s[:max_line_length] for s in text.splitlines()]

        y, x = self.get_global_pos((
            (
                pos[0],
                pos[0] - len(lines) // 2,
                (self.h - len(lines)) // 2
            )[center_v],
            (
                pos[1],
                pos[1],
                self.x_center
            )[center_h]
        ))

        tag = self.t.get_tag(fg, bg)
        try:
            if self.auto_flush:
                self.t.enable_write()
            for line in lines[:max_lines]:
                start_x = x - len(line) // 2 if center_h else x
                end_x = start_x + len(line)
                self.t.char_buffer[y][start_x:end_x] = list(line)
                self.t.fg_buffer[y][start_x:end_x].fill(fg)
                self.t.bg_buffer[y][start_x:end_x].fill(bg)
                if self.auto_flush:
                    self.t.text_widget.delete(self.t.widget_format((y, start_x)),
                                              self.t.widget_format((y, end_x)))
                    self.t.text_widget.insert(self.t.widget_format((y, start_x)), line, (tag,))
                y += 1
            if self.auto_flush:
                self.t.disable_write()
        except TclError:
            if PRINT_TKINTER_ERRORS:
                print_exc()
            sys.exit()

    def clear(self, corner1=None, corner2=None, style='clear'):
        """Clear a rectangle.

        corner1 (optional) -- Defaults to top left of Surface.
        corner2 (optional) -- Defaults to bottom right of Surface.
        style (optional) -- Dictionary containing keys 'char', 'fg', and 'bg'.
                            The default is style['clear'].
        """
        y1, x1 = corner1 or (0, 0)
        y2, x2 = corner2 or (self.h - 1, self.w - 1)
        # w = abs(x2 - x1) + 1
        w = x2 - x1 + 1
        h = y2 - y1 + 1
        style = self.get_style(style)
        char = style.pop('char')
        self.print_at((y1, x1), '\n'.join(char * w for i in range(h)), style)
        # for y in range(y1, y2 + 1):
        #     self.print_at((y, x1), char * w, style)

    def flush_all(self):
        try:
            self.t.enable_write()
            for y in range(self.y1, self.y2 + 1):
                self.t.text_widget.delete(self.t.widget_format((y, self.x1)),
                                          self.t.widget_format((y, self.x2 + 1)))
                last_pos = None
                last_tag = None
                text_buffer = None
                for x in range(self.x1, self.x2 + 1):
                    pos = (y, x)
                    tag = self.t.get_tag(self.t.fg_buffer[pos], self.t.bg_buffer[pos])
                    if tag != last_tag:
                        if text_buffer:
                            self.t.text_widget.insert(last_pos, text_buffer, (last_tag,))
                        last_pos = self.t.widget_format(pos)
                        text_buffer = self.t.char_buffer[pos]
                        last_tag = tag
                    else:
                        text_buffer += self.t.char_buffer[pos]
                self.t.text_widget.insert(last_pos, text_buffer, (last_tag,))
            self.t.disable_write()
        except TclError:
            if PRINT_TKINTER_ERRORS:
                print_exc()
            sys.exit()
