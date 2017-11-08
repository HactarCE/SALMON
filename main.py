# from game import *
from scenes import *
from textwrap import dedent
import logging as l
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

MAIN_MENU = MenuScene("SALMON", ["NEW GAME", "CONTINUE",
                                 "ACHIEVEMENTS", "SETTINGS", "QUIT"], disabled=[1])

SETTINGS_MENU = MenuScene("SETTINGS", ["BACK", "KEYBINDS", "FONT"])


def main():
    global term
    term = Terminal(title="SALMON")
    while True:
        show_main_menu()


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
     show_font_selection
     ][SETTINGS_MENU.show(term)]()


def show_font_selection():
    FontSizeSelectionScene().show(term)


def show_keybinds():
    pass


if __name__ == '__main__':
    main()
