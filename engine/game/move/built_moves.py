from engine.game.move.move import Move
from engine.game.move.built_components import *

__all__ = ["punch", "triplepunch", "slash", "magic_bolt", "magic_blast"]

punch = Move("punch",
    None,
    [
    SingleTarget(),
    EnemiesOnly(),
    Damage(50, "physical")
    ])

triplepunch = Move("triple punch",
    None,
    [
    SingleTarget(),
    EnemiesOnly(),
    Repeat(3, Damage(50, "physical"))
    ])

slash = Move("slash",
    "image/icon/attack_icon.png",
    [
    SingleTarget(),
    EnemiesOnly(),
    ScaleDamage(30, "physical", 1.0, "attack")
    ])

magic_bolt = Move("magic-bolt",
    "image/icon/magic_bolt_icon.png",
    [
    SingleTarget(),
    EnemiesOnly(),
    ScaleDamage(30, "magic", 1.1, "magic")
    ])

magic_blast = Move("magic-blast",
    "image/icon/magic_blast_icon.png",
    [
    GroupTarget(),
    EnemiesOnly(),
    ScaleDamage(20, "magic", 0.4, "magic")
    ])