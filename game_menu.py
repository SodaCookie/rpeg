from pygame import image
import view
from text import Text, TextInfo
from button import Button, ButtonInfo
import objects.dungeon as dungeon
import objects.party as party

_has_opened = False

def open():
    global _has_opened, _body, _single_player, _button, _button_h, _button_p, _button_d, _dungeon, _party

    if not _has_opened:
        _has_opened = True
        _button = image.load("images/menu/button500x120.png").convert()
        _button_h = image.load("images/menu/button_h500x120.png").convert()
        _button_p = image.load("images/menu/button_p500x120.png").convert()
        _button_d = image.load("images/menu/button_d500x120.png").convert()
        _dungeon = dungeon.Dungeon("test")
        _party = party.Party([])
        _dungeon.start.generate()

    text_style = TextInfo(fontcolor=(255,255,255), fontsize=14, alignment=0, wrap=True, width=300);
    button_style = ButtonInfo(100, 20, _button, _button_h, _button_p, _button_d);

    resolution = view.get_resolution()

    event = _dungeon.start.get_event()
    _body = Text((50, 50), text_style, event.body)
    for i, choice in enumerate(event.get_choices(_party)):
        _single_player = Button((50, 300+i*20), None, None, text_style, button_style, True, "Single Player")



def close():
    global _body, _single_player

    _body.delete()
    _body = None

    _single_player.delete()
    _single_player = None