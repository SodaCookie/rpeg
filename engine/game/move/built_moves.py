"""Compilation of the moves built to be used in the game"""

from engine.game.move.move import Move
from engine.game.move.built_components import *
from engine.game.move.built_modifiers import *
from engine.game.effect.built_effects import *
from engine.serialization.serialization import deserialize

__all__ = ["MOVES"]

MOVES = {}
SKILL_TREE = {}
SKILL_TREE['attack'] = ['magic bolt', 'quick attack', 'blessing',
                        'stunning blow']
SKILL_TREE['magic bolt'] = ['firebolt', 'arcane blast']
SKILL_TREE['blessing'] = ['healing word', 'mark for death']
SKILL_TREE['stunning blow'] = ['cleave', 'bolster']
SKILL_TREE['quick attack'] = ['backstab', 'double stab']
SKILL_TREE['firebolt'] = []
SKILL_TREE['arcane blast'] = []
SKILL_TREE['healing word'] = []
SKILL_TREE['mark for death'] = []
SKILL_TREE['bolster'] = []
SKILL_TREE['cleave'] = []
SKILL_TREE['backstab'] = []
SKILL_TREE['double stab'] = []

MOVES = deserialize("data/moves.p")