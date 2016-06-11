from PyQt5 import QtGui, QtWidgets, QtCore

import assets.attributes

from editor.core.handler.handler import Handler
from editor.core.prompt.list_prompt import ListPrompt
from editor.meta.types import StrType, AttributeType
from engine.serialization.item import ItemDataManager
from engine.serialization.floor import FloorDataManager
from engine.serialization.monster import MonsterDataManager
from engine.serialization.dmanager import DataManager

class MenuHandler(Handler):
    """Class responsible for handling menu actions"""

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        # Member variables
        self.floor_dm = FloorDataManager()
        self.item_dm = ItemDataManager()
        self.monster_dm = MonsterDataManager()

        menubar = self.parent.menuBar()
        menubar.triggered.connect(self.dispatch_action)

    def dispatch_action(self, action):
        """Helper function to dispatch action"""
        if action.objectName() == "actionExit":
            self.action_exit()
        elif action.objectName() == "actionSave":
            self.action_save()
        elif action.objectName() == "actionAdd_Floor":
            self.action_add_floor()
        elif action.objectName() == "actionAdd_Rare_Item_Attribute":
            self.action_add_rare_item_attribute()
        elif action.objectName() == "actionAdd_Legendary_Item_Attribute":
            self.action_add_legendary_item_attribute()
        elif action.objectName() == "actionAdd_Unique_Item_Attribute":
            self.action_add_unique_item_attribute()
        elif action.objectName() == "actionAdd_Monster_Attribute":
            self.action_add_monster_attribute()
        elif action.objectName() == "actionAbout":
            self.action_about()

    def action_save(self):
        DataManager.writeall()

    def action_exit(self):
        self.parent.close()

    def action_add_floor(self):
        def assign_floor(floors):
            self.floor_dm.set(floors)
            self.parent.scenario_handler.load_floors()
            self.parent.monster_handler.load_floors()
        prompt = ListPrompt(self.parent, StrType(),
            self.floor_dm.floors(), assign_floor)
        prompt.show()

    def action_add_rare_item_attribute(self):
        def assign_attribute(attributes):
            self.item_dm.set_rare_attributes({})
            for attr in attributes:
                self.item_dm.rare_attributes()[attr.name] = attr

        prompt = ListPrompt(self.parent, AttributeType(),
            self.item_dm.rare_attributes(), assign_attribute)
        prompt.show()

    def action_add_legendary_item_attribute(self):
        def assign_attribute(attributes):
            self.item_dm.set_legendary_attributes({})
            for attr in attributes:
                self.item_dm.legendary_attributes()[attr.name] = attr

        prompt = ListPrompt(self.parent, AttributeType(),
            self.item_dm.legendary_attributes(), assign_attribute)
        prompt.show()

    def action_add_unique_item_attribute(self):
        def assign_attribute(attributes):
            self.item_dm.set_unique_attributes({})
            for attr in attributes:
                self.item_dm.unique_attributes()[attr.name] = attr

        prompt = ListPrompt(self.parent, AttributeType(),
            self.item_dm.unique_attributes(), assign_attribute)
        prompt.show()

    def action_add_monster_attribute(self):
        def assign_attribute(attributes):
            self.monster_dm.set_attributes(attributes)

        prompt = ListPrompt(self.parent, AttributeType(),
            self.monster_dm.attributes(), assign_attribute)
        prompt.show()

    def action_about(self):
        with open("editor/data/editor_about", "r") as file:
            QtWidgets.QMessageBox.about(self.parent, "About", file.read())