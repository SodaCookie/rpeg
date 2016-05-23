from itertools import chain
from random import choice
import xml.etree.ElementTree as tree
import re

import engine.game.dungeon.dialog as dialog
from data.scenarios import EVENTS

class Location(object):
	"""Location object is the node for each part of a dungeon"""

	def __init__(self, room_type, floor_type):
		# can be event, entrance, exit, shop, alter, item
		self.room_type = room_type
		self.floor_type = floor_type
		# self.locked = False # to be implemented
		# self.blocked = False # to be implemented
		self.event = None
		self.neighbours = []

	def get_event(self):
		"""Returns the event found at this location"""
		return "main"

	def get_dialogue(self, name):
		return self.event.dialogues.get(name)

	def get_event_name(self):
		return self.event.name

	# def set_block(self):
	# 	self.blocked = True

	# def set_lock(self):
	# 	self.locked = True

	def set_type(self, room_type):
		self.room_type = room_type

	def set_neighbour(self, location):
		self.neighbours.append(location)

	def get_neighbours(self):
		return self.neighbours

	def generate(self):
		"""Method is used to generate a suitable event based
		on room_type and floor_type"""
		# Gather a list of available events
		available = []
		available.extend(EVENTS["any"][self.room_type])
		available.extend(EVENTS[self.floor_type][self.room_type])

		self.event = choice(available)

	def __repr__(self):
		return self.room_type


if __name__ == "__main__":
	#from lxml import etree as tree #optional version of the tree in case we need faster parsing
	with open("data/scenario.xml", "r") as file:
		etree = tree.parse(file)
	loc = Location("event", "test")
	loc.generate(etree)
	print(loc.description)