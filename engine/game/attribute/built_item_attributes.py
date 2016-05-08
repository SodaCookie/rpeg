"""Compilation of attributes that can be used for items. Some will be unique
for unique items. Some will be classified as available for rare items, Some
will be classified as available for legendary items."""

import os

from engine.serialization import serialization as serial
from engine.game.attribute.built_attributes import *

RARE_ATTRIBUTES = {}
LEGENDARY_ATTRIBUTES = {}
UNIQUE_ATTRIBUTES = {}

# LOAD RARE ATTRIBUTES
path = "data/item/attributes/rare/"
for file in os.listdir(path):
    name = file.split(".")[0].replace("_", " ")
    RARE_ATTRIBUTES[name] = serial.deserialize(path + file)

# LOAD LEGENDARY ATTRIBTUES
path = "data/item/attributes/legendary/"
for file in os.listdir(path):
    name = file.split(".")[0].replace("_", " ")
    LEGENDARY_ATTRIBUTES[name] = serial.deserialize(path + file)

# LOAD UNIQUE ATTRIBUTES
path = "data/item/attributes/unique/"
for file in os.listdir(path):
    name = file.split(".")[0].replace("_", " ")
    UNIQUE_ATTRIBUTES[name] = serial.deserialize(path + file)
