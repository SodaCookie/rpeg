"""Compilation of attributes that can be used for items. Some will be unique
for unique items. Some will be classified as available for rare items, Some
will be classified as available for legendary items."""

import os

from engine.serialization import serialization as serial
from engine.game.attribute.built_attributes import *

RARE_ATTRIBUTES = {}
LEGENDARY_ATTRIBUTES = {}
UNIQUE_ATTRIBUTES = {}

# LOAD ATTRIBUTES
RARE_ATTRIBUTES = serial.deserialize("data/item/attributes/rare_attributes.p")
LEGENDARY_ATTRIBUTES = serial.deserialize("data/item/attributes/legendary_attributes.p")
UNIQUE_ATTRIBUTES = serial.deserialize("data/item/attributes/unique_attributes.p")