from engine.game.move.move import Move
from engine.game.move.built_components import *

punch = Move("punch",
    [
    SingleTarget(),
    EnemiesOnly(),
    Damage(50, "physical")
    ])

triplepunch = Move("triple punch",
    [
    SingleTarget(),
    EnemiesOnly(),
    Repeat(3, Damage(50, "physical"))
    ])