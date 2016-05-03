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
event_main = Dialogue(
    "main",
    "Your party is surrounded by monsters.",
    actions=[BattleAction()])

EVENTS["any"]["monster"].append(
    Event("Ambush!", event_main)
)

#=============================================================================#
#==========================        Catacombs       ===========================#
#=============================================================================#
EVENTS["catacombs"] = {}
EVENTS["catacombs"]["entrance"] = []
EVENTS["catacombs"]["exit"] = []
EVENTS["catacombs"]["event"] = []
EVENTS["catacombs"]["monster"] = []

#============================== ENTRANCE EVENT ===============================#
event_main = Dialogue(
    "main",
    "The Catacombs, once a place to rest the bodies of those who pasted on. Now a cesspool for necromancers, grave robbers and abominations alike. Hoards of undead and terrifying creatures await you at every turn. Trend carefully.")

EVENTS["catacombs"]["entrance"].append(
    Event("The Catacombs", event_main)
)

#=============================== GHOST EVENT =================================#
promise = Dialogue(
    "Promise to defeat the Necromancer",
    "The spirits are pleased by your promise of good will. They give your party shards to help you on your quest.",
    actions=[LootAction(shards=100)])

approach_help_fail = Dialogue(
    "approach_help_fail",
    "\"No, no, you can't help us! Tricks, more tricks!\"\n\nThe spirits refuse your offer of help. They shriek curses at your party as they turn to fight you.",
    actions=[BattleAction()])

approach_help = Dialogue(
    "How can we help you?",
    "\"Please, the Necromancer has sealed these catacombs, none who are dead can escape it and find peace.\"",
    choices=[promise],
    chance=80,
    fail=approach_help_fail)

approach_abandon = Dialogue(
    "You're on your own.",
    "\"Why, why won't you help us?\"\n\nTheir wails turn to screeches and dash angrily towards your party!",
    actions=[BattleAction()])

approach = Dialogue(
    "Approach the lost spirits",
    "Your party cautiously walks towards the spirits. They notice your presence and turn to confront you.\n\n\"Help, can you please help us?\"",
    choices=[approach_help, approach_abandon])

leave_fail = Dialogue(
            "leave_fail",
            "Suddenly, the spirit notice you're presence. Their wails turn to screeches as they dash angrily towards your party!\n\n\"Why won't anyone help us?!?\"",
            actions=[BattleAction()])

leave = Dialogue(
    "Leave them be",
    "Your party decides to leave them be. As you and the spirits take separate path down the catacombs, you hear their moans grow increasingly distant.",
    chance=50,
    fail=leave_fail)

event_main = Dialogue(
    "main",
    "You see wandering spirits ahead of your party. Shimmering in the distance you can hear them moaning and wailing.\n\n\"I can't see the light\"\n\nAs they slowly drift aimlessly.",
    choices=[leave, approach])

EVENTS["catacombs"]["event"].append(
    Event("Lost Spirits", event_main)
)

