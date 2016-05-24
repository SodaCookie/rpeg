from functools import lru_cache

from PyQt5 import QtGui, QtWidgets, QtCore

import assets.moves
import assets.moves.components
import assets.moves.modifiers

from editor.core.class_prompt import ClassPrompt
from engine.serialization.serialization import deserialize

class MonsterHandler:

    def __init__(self, parent):
        self.parent = parent
        self.MOVES = deserialize("data/moves.p")
        self.init_monster()
        self.current_focus = None

    def load_monster