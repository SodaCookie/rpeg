import os

from engine.serialization import serialization as serial
from engine.game.item.item import Item

BASE_ITEMS = {}
ITEMS = {}

# LOAD BASE ITEMS
path = "data/item/base/"
for file in os.listdir(path):
    name = file.split(".")[0].replace("_", " ")
    BASE_ITEMS[name] = serial.deserialize(path + file)

# LOAD ITEMS
path = "data/item/built/"
for file in os.listdir(path):
    name = file.split(".")[0].replace("_", " ")
    ITEMS[name] = serial.deserialize(path + file)
