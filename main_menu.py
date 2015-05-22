from pygame import image
import view
from text import Text, TextInfo
from button import Button, ButtonInfo
import game_menu

_has_opened = False

def open(on_sp, on_mp):
    global _has_opened, _title, _single_player, _multi_player, _button, _button_h, _button_p, _button_d

    if not _has_opened:
        _has_opened = True
        _button = image.load("images/menu/button500x120.png").convert()
        _button_h = image.load("images/menu/button_h500x120.png").convert()
        _button_p = image.load("images/menu/button_p500x120.png").convert()
        _button_d = image.load("images/menu/button_d500x120.png").convert()


    text_style = TextInfo(fontcolor=(255,255,255), fontsize=50, h_anchor=0, v_anchor=0, alignment=0);
    button_style = ButtonInfo(500, 120, _button, _button_h, _button_p, _button_d);

    resolution = view.get_resolution()

    _title = Text((resolution[0] / 2, resolution[1] / 4), text_style, "RNG Kitty Blaster")
    _single_player = Button((resolution[0] / 2, resolution[1] / 2), on_sp, None, text_style, button_style, True, "Single Player")
    _multi_player = Button((resolution[0] / 2, resolution[1] / 4 * 3), on_mp, None, text_style, button_style, True, "Multi Player")



def close():
    global _title, _single_player, _multi_player

    _title.delete()
    _title = None

    _single_player.delete()
    _single_player = None

    _multi_player.delete()
    _multi_player = None

    game_menu.open()
