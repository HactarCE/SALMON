# from game import *
from scenes import *
from textwrap import dedent
import logging as l
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    global term
    term = Terminal(title="SALMON")
    show_main_menu()


def show_main_menu():
    callbacks = [new_game, continue_game, show_achievements, show_settings, sys.exit]
    choices = ["NEW GAME", "CONTINUE", "ACHIEVEMENTS", "SETTINGS", "QUIT"]
    MenuScene("SALMON", choices, lambda choice: callbacks[choice](), [1]).show(term)


def new_game():
    ExpositionScene(dedent('''\
    You can't start a new game. I haven't implemented that yet!

    But you know what I have implemented? Text wrapping! And that's what's happening right now. This paragraph is so long that it'll wrap to the next line! Isn't that awesome? Don't thank me; thank textwrap.fill() for producing this wonderful feature.

    Text centering was all me though.
    '''), "TITLE").show(term)
    show_main_menu()


def continue_game():
    ExpositionScene(dedent('''\
    You can't continue. I haven't implemented that yet!
    (Also you shouldn't be able to select this.)
    ''')).show(term)
    show_main_menu()


def show_achievements():
    ExpositionScene(dedent('''\
    You can't view achievements.
    I haven't implemented that yet!
    ''')).show(term)
    show_main_menu()


def show_settings():
    current = term.get_font_size()
    new = current + 2 if current < 24 else 8
    ExpositionScene(dedent('''\
    You can't change settings. I haven't implemented that yet!

    So for now this button just cycles through font sizes.
    Current font size: {}
    New font size: {}
    ''').format(current, new)).show(term)
    term.set_font_size(new)
    show_main_menu()

if __name__ == '__main__':
    main()
