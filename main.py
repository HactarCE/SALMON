#!/usr/bin/env python3

from gamedata import areas, items
from textwrap import dedent
from traceback import print_exc
from terminal import Terminal
from tui import Menu, SpinnerChoice, Text, Game
import os
import saveload

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    global term, surf
    term = Terminal(title="SALMON")
    surf = term.surface()
    surf.styles['default']['center_h'] = 2
    surf.styles['content']['center_v'] = 2
    # surf.styles['default']['center_v'] = 2
    try:
        saveload.load_settings(term)
    except:
        print_exc()
    build_menus()
    # doesn't work when compiled for some reason
    # term.root.iconbitmap(os.path.join(os.path.dirname(
    # os.path.realpath(__file__)), r'icon\icon.ico'))
    while True:
        show_main_menu()


def build_menus():
    global MAIN_MENU, SETTINGS_MENU, FONT_MENU
    MAIN_MENU = Menu("SALMON",
                     ["NEW GAME", "CONTINUE", "ACHIEVEMENTS", "SETTINGS", "QUIT"],
                     disabled_choices=[1])
    SETTINGS_MENU = Menu("SETTINGS",
                         ["BACK", SpinnerChoice(
                             ['HELP SCREEN: ON', 'HELP SCREEN: OFF'],
                             'HELP SCREEN: O' + ('N' if saveload.show_help_screen else 'FF'),
                             lambda choice: set_help_screen(choice.endswith('ON'))),
                          "FONT"])
    FONT_MENU = None  # set it when ya need it, thanks


def set_help_screen(is_on):
    if is_on != saveload.show_help_screen:
        saveload.show_help_screen = is_on
        saveload.save_settings(term)


def show_main_menu():
    [new_game,
     continue_game,
     show_achievements,
     show_settings,
     term.quit][MAIN_MENU.show(surf)]()


def new_game():
    # Text(dedent('''\
    # You can't start a new game. I haven't implemented that yet!
    #
    # But you know what I have implemented? Text wrapping! And that's what's happening right now. This paragraph is so long that it'll wrap to the next line! Isn't that awesome? Don't thank me; thank textwrap.fill() for producing this wonderful feature.
    #
    # Text centering was all me though.
    # '''), "TITLE").show(surf)
    # Hotbar(lambda i: None).show(surf, 1)
    # term.wait_for_key_press()
    Game({
        'hotbar': [
            None, None, None,
            items.teleporter.Teleporter([
                areas.start.START,
                areas.demo.DEMO_1,
                areas.demo.DEMO_2,
                areas.demo.DEMO_3
            ]), None, None
        ]
    }).show(surf)


def continue_game():
    Text(dedent('''\
    You can't continue. I haven't implemented that yet!
    (Also you shouldn't be able to select this.)
    ''')).show(surf)


def show_achievements():
    Text(dedent('''\
    You can't view achievements.
    I haven't implemented that yet!
    ''')).show(surf)


def show_settings():
    loop = True
    while loop:
        selection = SETTINGS_MENU.show(surf)
        loop = selection > 0
        [lambda: None,
         # show_keybinds,
         lambda: None,
         show_font_selection,
         lambda: None
         ][selection]()


def show_font_selection():
    global FONT_MENU
    if not FONT_MENU:
        Text("Loading fonts...", None, None).show(surf, loop=False)
        term.update()
        fonts = term.get_fixed_fonts()
        current_font_fam = term.get_font()['family']
        current_selection = None
        for i in range(len(fonts)):
            if fonts[i]['family'] == current_font_fam:
                current_selection = fonts[i]
        font_sizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 24]
        FONT_MENU = Menu("FONT OPTIONS",
                         ["SAVE CHANGES",
                          SpinnerChoice(fonts, current_selection,
                                        lambda choice: term.set_font(choice),
                                        lambda f: f['family']),
                          SpinnerChoice(font_sizes, term.get_font_size(),
                                        lambda choice: term.set_font_size(choice))])
    old_font, old_font_size = term.get_font(), term.get_font_size()
    if FONT_MENU.show(surf) == -1:
        term.set_font(old_font, old_font_size)
    else:
        saveload.save_settings(term)
    # FontSizeSelectionScene().show(term)


def show_keybinds():
    Text("Keybind customization\nhasn't been implemented yet.").show(term)


if __name__ == '__main__':
    main()
