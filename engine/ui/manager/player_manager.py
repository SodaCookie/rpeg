from engine.ui.core.manager import Manager

from engine.ui.element.button import Button

class PlayerManager(Manager):

    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.add_renderable(Button("Test", text="TESTING", width=100, height=100))