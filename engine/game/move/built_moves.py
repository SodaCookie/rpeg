"""Compilation of the moves built to be used in the game"""

from engine.game.move.move import Move
from engine.game.move.built_components import *
from engine.game.move.built_modifiers import *
from engine.game.effect.built_effects import *

__all__ = ["PLAYER_MOVES", "MONSTER_MOVES"]

MONSTER_MOVES = {}
PLAYER_MOVES = {}

# PLAYER MOVE SEGMENT

# TESTED UNSURE ABOUT CRIT FUNCTIONALITY
PLAYER_MOVES["attack"] = Move("attack",
    None,
    [
    TargetOneOnly(),
    SingleTarget(),
    EnemiesOnly(),
    Damage(0, "physical",
        [
        ScaleStat(1, "attack"),
        ScaleLevel(1)
        ])
    ],
    crit_bound = 90,
    crit_components = [
    TargetOneOnly(),
    SingleTarget(),
    EnemiesOnly(),
    Damage(0, "physical",
        [
        ScaleStat(1, "attack"),
        ScaleLevel(2),
        ])
    ])

# TESTED
PLAYER_MOVES["magic bolt"] = Move("magic bolt",
    None,
    [
    TargetOneOnly(),
    SingleTarget(),
    EnemiesOnly(),
    Damage(0, "magic",
        [
        ScaleStat(1, "magic"),
        ScaleLevel(1)
        ])
    ])

# TESTED
PLAYER_MOVES["blessing"] = Move("blessing",
    None,
    [
    TargetOneOnly(),
    SingleTarget(),
    AlliesOnly(),
    AddEffect(StatChange("blessing", 5, "attack", 6))
    ])

# TESTED
PLAYER_MOVES["stunning blow"] = Move("stunning blow",
    None,
    [
    TargetOneOnly(),
    SingleTarget(),
    EnemiesOnly(),
    AddChanceEffect(Stun(5), 0.2),
    Damage(0, "physical",
        [
        ScaleStat(1, "attack"),
        ScaleLevel(0.8),

        ])
    ],
    crit_bound = 90,
    crit_components = [
    TargetOneOnly(),
    SingleTarget(),
    EnemiesOnly(),
    AddChanceEffect(Stun(5), 0.2),
    Damage(0, "physical",
        [
        ScaleStat(2, "attack"),
        ScaleLevel(1),
        ])
    ])

# TESTED
PLAYER_MOVES["quick attack"] = Move("quick attack",
    None,
    [
    TargetOneOnly(),
    SingleTarget(),
    EnemiesOnly(),
    SelfEffect(StatChangeTilMove("haste", 5, "speed")),
    Damage(0, "physical",
        [
        ScaleStat(1, "attack"),
        ScaleLevel(0.8),
        ])
    ],
    crit_bound = 90,
    crit_components = [
    TargetOneOnly(),
    SingleTarget(),
    EnemiesOnly(),
    SelfEffect(StatChangeTilMove("haste", 5, "speed")),
    Damage(0, "physical",
        [
        ScaleStat(2, "attack"),
        ScaleLevel(1),
        ])
    ])

## NEEDS DOT EFFECT
# PLAYER_MOVES["firebolt"] = Move("firebolt",
#     None,
#     [
#     TargetOneOnly(),
#     SingleTarget(),
#     EnemiesOnly(),
#     Damage(0, "magic",
#         [
#         ScaleStat(1, "magic"),
#         ScaleLevel(0.6)
#         ])
#     ],
#     crit_bound = 50,
#     crit_components = [
#     TargetOneOnly(),
#     SingleTarget(),
#     EnemiesOnly(),
#     Damage(0, "magic",
#         [
#         ScaleStat(1, "magic"),
#         ScaleLevel(0.6)
#         ]),
#     AddEffect()
#     ])

# TESTED
PLAYER_MOVES["arcane blast"] = Move("arcane blast",
    None,
    [
    TargetOneOnly(),
    GroupTarget(),
    EnemiesOnly(),
    Damage(0, "magic",
        [
        ScaleStat(1, "magic"),
        ScaleLevel(0.4)
        ])
    ])

# TESTED
PLAYER_MOVES["healing word"] = Move("healing word",
    None,
    [
    TargetOneOnly(),
    SingleTarget(),
    Heal(10, [
        ScaleLevel(1)
        ])
    ])

PLAYER_MOVES["mark for death"] = Move("mark for death",
    None,
    [
    TargetOneOnly(),
    SingleTarget(),
    EnemiesOnly(),
    AddEffect(StatChange("marked", -5, "defense", 10))
    ])

# SHOULD TARGET SELF ONLY
# PLAYER_MOVES["bolster"] = Move("bolster",
#     None,
#     [
#     sometargetscheme()
#     SelfEffect(StatChange("bolstered", 5, "defense", 8))
#     ])


PLAYER_MOVES["cleave"] = Move("cleave",
    None,
    [
    TargetNumberOnly(2),
    EnemiesOnly(),
    Damage(0, "physical",
        [
        ScaleStat(1, "attack"),
        ScaleLevel(0.6),
        ])
    ],
    crit_bound = 90,
    crit_components = [
    TargetOneOnly(),
    SingleTarget(),
    EnemiesOnly(),
    Damage(0, "physical",
        [
        ScaleStat(2, "attack"),
        ScaleLevel(0.6),
        ])
    ])

# IGNORES DEFENSE OF STUNNED TARGET
# PLAYER_MOVES["backstab"] = Move("backstab",
#     None,
#     [
#     TargetOneOnly(),
#     EnemiesOnly(),
#     someignoredefense()
#     Damage(0, "physical",
#         [
#         ScaleStat(1, "attack"),
#         ScaleLevel(1),
#         ])
#     ],
#     crit_bound = 90,
#     crit_components = [
#     TargetOneOnly(),
#     SingleTarget(),
#     EnemiesOnly(),
#     someignoredefense()
#     Damage(0, "physical",
#         [
#         ScaleStat(1, "attack"),
#         ScaleLevel(1),
#         ScaleCrit(3)
#         ])
#     ])

PLAYER_MOVES["double stab"] = Move("double stab",
    None,
    [
    TargetOneOnly(),
    SingleTarget(),
    EnemiesOnly(),
    Repeat(2,
        Damage(0, "physical",
            [
            ScaleStat(1, "attack"),
            ScaleLevel(0.6)
            ])
        )
    ],
    crit_bound = 90,
    crit_components = [
    TargetOneOnly(),
    SingleTarget(),
    EnemiesOnly(),
    ScaleCrit(2),
    Repeat(2,
        Damage(0, "physical",
            [
            ScaleStat(2, "attack"),
            ScaleLevel(0.6)
            ])
        )
    ])

# MONSTER MOVE SEGMENT

MONSTER_MOVES["attack"] = Move("punch",
    None,
    [
    RandomEnemyTarget(),
    EnemiesOnly(),
    Damage(0, "physical",
        [
        ScaleStat(1, "attack"),
        ])
    ])