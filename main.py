# from game import *
from scenes import *
from textwrap import dedent
from tkinter import font as tkFont
import saveload

import logging as l
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    global term
    term = Terminal(title="SALMON")
    build_menus()
    try:
        saveload.load_settings(term)
    except:
        pass
    # term.root.iconbitmap(os.path.join(os.path.dirname(os.path.realpath(__file__)),
    # r'icon\icon.ico')) # doesn't work when compiled for some reason
    while True:
        show_main_menu()


def build_menus():
    global MAIN_MENU, SETTINGS_MENU, FONT_MENU
    MAIN_MENU = MenuScene("SALMON", ["NEW GAME", "CONTINUE",
                                     "ACHIEVEMENTS", "SETTINGS", "QUIT"], disabled=[1])
    SETTINGS_MENU = MenuScene("SETTINGS", ["BACK", "KEYBINDS", "FONT"])
    FONT_MENU = None  # set it when ya need it, thanks


def show_main_menu():
    [new_game,
     continue_game,
     show_achievements,
     show_settings,
     term.quit][MAIN_MENU.show(term)]()


def new_game():
    ExpositionScene(dedent('''\
    You can't start a new game. I haven't implemented that yet!

    But you know what I have implemented? Text wrapping! And that's what's happening right now. This paragraph is so long that it'll wrap to the next line! Isn't that awesome? Don't thank me; thank textwrap.fill() for producing this wonderful feature.

    Text centering was all me though.
    '''), "TITLE").show(term)


def continue_game():
    ExpositionScene(dedent('''\
    You can't continue. I haven't implemented that yet!
    (Also you shouldn't be able to select this.)
    ''')).show(term)


def show_achievements():
    ExpositionScene(dedent('''\
    You can't view achievements.
    I haven't implemented that yet!
    ''')).show(term)


def show_settings():
    [lambda: None,
     show_keybinds,
     show_font_selection,
     lambda: None
     ][SETTINGS_MENU.show(term)]()


def show_font_selection():
    global FONT_MENU
    if not FONT_MENU:
        term.clear()
        term.print_centered(None, 'Loading fonts...')
        term.redraw()
        fonts = term.get_fixed_fonts()
        current_font_fam = term.get_font()['family']
        current_selection = None
        for i in range(len(fonts)):
            if fonts[i]['family'] == current_font_fam:
                current_selection = fonts[i]
        font_sizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 24]
        FONT_MENU = MenuScene("FONT OPTIONS", ["SAVE CHANGES",
                                       SpinnerChoice(fonts, current_selection,
                                                     lambda choice: (term.set_font(choice), term.redraw()),
                                                     lambda f: f['family']),
                                       SpinnerChoice(font_sizes, term.get_font_size(),
                                                     lambda choice: term.set_font_size(choice))])
    old_font, old_font_size = term.get_font(), term.get_font_size()
    if FONT_MENU.show(term) == -1:
        term.set_font(old_font, old_font_size)
    else:
        saveload.save_settings(term)
    # FontSizeSelectionScene().show(term)


def show_keybinds():
    term.clear()
    term.print_centered(None, "Keybind customization\nhasn't been implemented yet.")
    term.redraw()
    term.wait_for_key_press()


if __name__ == '__main__':
    main()
