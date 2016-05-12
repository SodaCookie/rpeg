import os

from engine.serialization import serialization as serial
from engine.game.item.item import Item

BASE_ITEMS = {}
ITEMS = {}

#LOAD ITEMS
BASE_ITEMS = serial.deserialize("data/item/base_items.p")
ITEMS = serial.deserialize("data/item/items.p")