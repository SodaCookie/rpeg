from engine.ui.core.manager import Manager

from engine.ui.element.button import Button
from engine.ui.element.frame import Frame
from engine.ui.element.text import Text
from engine.ui.element.itemslot import ItemSlot

from engine.game.item.item_factory import ItemFactory

class PlayerManager(Manager):

    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.test = [ItemFactory.static_generate("iron plating"), None, None, None, None]
        self.add_renderable(Button("Test", text="TESTING", width=100, height=100, on_click=lambda game, system: print("hello")))
        self.add_renderable(Frame("test2", 200, 200, 100, 100))
        self.add_renderable(Text("test3", 300, 300, "tests a longer string a really, really, really, really, really, really, really, really, really, really, really, really, really, really long string", 18, width=300))
        self.add_renderable(ItemSlot("itemtest", 0, 200, "any", (self.test, 0), lambda value: print(self.test)))
        self.add_renderable(ItemSlot("itemtest2", 0, 260, "any", (self.test, 1), lambda value: print(self.test)))
        self.add_renderable(ItemSlot("itemtest3", 0, 320, "any", (self.test, 2), lambda value: print(self.test)))
        self.add_renderable(ItemSlot("itemtest4", 0, 380, "any", (self.test, 3), lambda value: print(self.test)))
        self.add_renderable(ItemSlot("itemtest5", 0, 440, "any", (self.test, 4), lambda value: print(self.test)))
