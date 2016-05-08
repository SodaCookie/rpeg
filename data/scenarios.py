from assets.actions import *
from assets.conditions import *
from engine.game.dungeon.event import Event
from engine.game.dungeon.dialog import Dialogue

# EVENTS[<floor>][<room>]
EVENTS = {}

#=============================================================================#
#==========================           Any          ===========================#
#=============================================================================#
EVENTS["any"] = {}
EVENTS["any"]["entrance"] = []
EVENTS["any"]["exit"] = []
EVENTS["any"]["event"] = []
EVENTS["any"]["monster"] = []

#============================== STANDARD BATTLE ==============================#

event = Event("Ambush!")
EVENTS["any"]["monster"].append(event)

event.add_dialogue(Dialogue(
    "main",
    "",
    "Your party is surrounded by monsters.",
    actions=[BattleAction()]))

#=============================================================================#
#==========================        Catacombs       ===========================#
#=============================================================================#
EVENTS["catacombs"] = {}
EVENTS["catacombs"]["entrance"] = []
EVENTS["catacombs"]["exit"] = []
EVENTS["catacombs"]["event"] = []
EVENTS["catacombs"]["monster"] = []

#============================== ENTRANCE EVENT ===============================#

event = Event("The Catacombs")
EVENTS["catacombs"]["entrance"].append(event)

event.add_dialogue(Dialogue(
    "main",
    "",
    "The Catacombs, once a place to rest the bodies of those who pasted on. Now a cesspool for necromancers, grave robbers and abominations alike. Hoards of undead and terrifying creatures await you at every turn. Trend carefully."))


#=============================== GHOST EVENT =================================#

event = Event("Lost Spirits")
EVENTS["catacombs"]["event"].append(event)

event.add_dialogue(Dialogue(
    "promise",
    "Promise to defeat the Necromancer",
    "The spirits are pleased by your promise of good will. They give your party shards to help you on your quest.",
    actions=[LootAction(shards=100)]))

event.add_dialogue(Dialogue(
    "approach_help_fail",
    "",
    "\"No, no, you can't help us! Tricks, more tricks!\"\n\nThe spirits refuse your offer of help. They shriek curses at your party as they turn to fight you.",
    actions=[BattleAction()]))

event.add_dialogue(Dialogue(
    "approach_help",
    "How can we help you?",
    "\"Please, the Necromancer has sealed these catacombs, none who are dead can escape it and find peace.\"",
    choices=["promise"],
    chance=80,
    fail="approach_help_fail"))

event.add_dialogue(Dialogue(
    "approach_abandon",
    "You're on your own.",
    "\"Why, why won't you help us?\"\n\nTheir wails turn to screeches and dash angrily towards your party!",
    actions=[BattleAction()]))

event.add_dialogue(Dialogue(
    "approach",
    "Approach the lost spirits",
    "Your party cautiously walks towards the spirits. They notice your presence and turn to confront you.\n\n\"Help, can you please help us?\"",
    choices=["approach_help", "approach_abandon"]))

event.add_dialogue(Dialogue(
    "leave_fail",
    "",
    "Suddenly, the spirit notice you're presence. Their wails turn to screeches as they dash angrily towards your party!\n\n\"Why won't anyone help us?!?\"",
    actions=[BattleAction()]))

event.add_dialogue(Dialogue(
    "leave",
    "Leave them be",
    "Your party decides to leave them be. As you and the spirits take separate path down the catacombs, you hear their moans grow increasingly distant.",
    chance=50,
    fail="leave_fail"))

event.add_dialogue(Dialogue(
    "main",
    "",
    "You see wandering spirits ahead of your party. Shimmering in the distance you can hear them moaning and wailing.\n\n\"I can't see the light\"\n\nAs they slowly drift aimlessly.",
    choices=["leave", "approach"]))


