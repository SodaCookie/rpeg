import view
from image_cache import ImageCache
from text import Text, TextInfo
from button import Button, ButtonInfo
import objects.dungeon as dungeon
import objects.party as party
import copy

class GameMenu(object):
    def __init__(self):
        button = ImageCache.add("images/menu/button500x120.png")
        button_h = ImageCache.add("images/menu/button_h500x120.png")
        button_p = ImageCache.add("images/menu/button_p500x120.png")
        button_d = ImageCache.add("images/menu/button_d500x120.png")
        self.dungeon = dungeon.Dungeon("test")
        self.party = party.Party([])
        self.choices = []
        self.dungeon.start.generate()
        
        text_style = TextInfo(fontcolor=(255,255,255), fontsize=20, alignment=0, h_anchor=0, v_anchor=0, wrap=True, width=300);
        button_style = ButtonInfo(500, 14, (255, 255, 255), (255, 255, 0), (0, 128, 0), (0, 0, 0), None, None, None, None);

        resolution = view.get_resolution()

        event = self.dungeon.start.get_event()
        self.body = Text((resolution[0]/4, 50), text_style, event.body)
        for i, choice in enumerate(event.get_choices(self.party)):
            self.choices.append(Button((resolution[0]/4, 300+i*50), None, None, copy.copy(text_style), copy.copy(button_style), True, choice))

    def close(self):
        self.body.delete()
        for i in self.choices:
            i.delete()
