import random
import action

class Dialog(object):
  """Dialog object is used to keep track of possible text"""

  def __init__(self, name, etree):
    self.name = name
    self.body = "" # used to describe what is happening
    self.choices = {} # key is the choice text the value is the list of other dialogs, if choices is empty default to next
    self.condition = lambda party: True # used to check to see this dialog is available to the party
    self.chance = 100 # chance that this dialog will be successful
    self.fail = None
    self.action = None

    dialog = etree.find("dialog[@name='%s']"%name)
    if dialog is not None:
        if dialog.find("body") is not None:
          self.body = "\n".join([line.lstrip() for line in dialog.find("body").text.split('\n')]) # split remove all leading whitespace then merge again
        if dialog.find("choices") is not None:
          self.choices = {choice.text: Dialog(choice.attrib["name"], etree) for choice in dialog.findall("choices/choice")}
        if dialog.find("condition") is not None:
          self.condition = dialog.find("condition").text
        if dialog.find("chance") is not None:
          self.chance = int(dialog.find("chance").text)
          if dialog.find("chance").attrib.get("fail") is not None:
            self.fail = Dialog(dialog.find("chance").attrib["fail"], etree)
            print(self.name, self.fail.name)
        if dialog.find("action") is not None:
          self.action = dialog.find("action").text
    elif name == "main":
      raise Exception("Could not find 'main' dialog")

  def roll(self):
    """See if was successful"""
    if random.randint(1,100) < self.chance:
      return True
    return False

  def get_choices(self, party):
    """get the available choices based on the party"""
    return self.choices # to be implemented

  def make_choice(self, choice):
    """Returns the dialogue that was chosen, if every roll fails it will default to returning the last roll"""
    choice = self.choices[choice]
    if choice.fail is None: # just to make sure im not dumb >.<
      return choice # in the event that a single choice is given a chance with fail dialog
    while not choice.roll(): # while keep failing
      choice = choice.fail
      if choice.fail is None: # leave if there are not other fallbacks
        break
    return choice

if __name__ == "__main__":
  import xml.etree.ElementTree as tree
  #from lxml import etree as tree #optional version of the tree in case we need faster parsing
  with open("data/test_data.xml", "r") as file:
    etree = tree.parse(file)
  d = Dialog("main", etree.find("event[@name='sword_event']"))