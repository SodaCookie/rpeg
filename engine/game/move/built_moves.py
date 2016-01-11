"""Compilation of the moves built to be used in the game"""

from engine.game.move.move import Move
from engine.game.move.built_components import *

__all__ = ["PLAYER_MOVES", "MONSTER_MOVES"]

MONSTER_MOVES = {}
PLAYER_MOVES = {}

PLAYER_MOVES["punch"] = Move("punch",
    None,
    [
    SingleTarget(),
    EnemiesOnly(),
    Damage(50, "physical")
    ])

PLAYER_MOVES["triple punch"] = Move("triple punch",
    None,
    [
    SingleTarget(),
    EnemiesOnly(),
    Repeat(3, Damage(50, "physical"))
    ])

PLAYER_MOVES["slash"] = Move("slash",
    "image/icon/attack_icon.png",
    [
    SingleTarget(),
    EnemiesOnly(),
    ScaleDamage(30, "physical", 1.0, "attack")
    ])

PLAYER_MOVES["magic-bolt"] = Move("magic-bolt",
    "image/icon/magic_bolt_icon.png",
    [
    SingleTarget(),
    EnemiesOnly(),
    ScaleDamage(30, "magic", 1.1, "magic")
    ])

PLAYER_MOVES["magic-blast"] = Move("magic-blast",
    "image/icon/magic_blast_icon.png",
    [
    GroupTarget(),
    EnemiesOnly(),
    ScaleDamage(20, "magic", 0.4, "magic")
    ])