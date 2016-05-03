import random

class Dialogue(object):
	"""Dialogue object is used to keep track of possible text"""

	def __init__(self, dtext, body, chance=100, fail=None, choices=None,
			conditions=None, actions=None):
		"""Creates a Dialogue object.
		name - an identifier to access the dialogue
		body - text to display onto the screen
		chance - chance to succeed where 100 is guaranteed
		fail - the dialogue to call if failed
		choices - a dictionary to access the children
		condition - conditions to access this choice
		action - """
		self.dtext = dtext # dialogue text (text for the choice)
		self.body = body
		self.chance = chance
		self.fail = fail
		self.choices = choices if choices else []
		self.conditions = conditions if conditions else []
		self.actions = actions if actions else []

	def get_available_choices(self, party):
		"""get the available choices based on the party"""
		available = []
		for choice in self.choices:
			if all(condition.apply(party) for condition in choice.conditions):
				available.append(choice)
		return available

	def get_actions(self):
		"""Return the list of actions"""
		return self.actions


if __name__ == "__main__":
	import xml.etree.ElementTree as tree
	#from lxml import etree as tree #optional version of the tree in case we need faster parsing
	with open("data/test_data.xml", "r") as file:
		etree = tree.parse(file)
	d = Dialog("main", etree.find("event[@name='sword_event']"))