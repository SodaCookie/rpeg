"""Compilation of the moves built to be used in the game"""

from engine.game.move.move import Move
from engine.game.move.built_components import *
from engine.game.move.built_modifiers import *
from engine.game.effect.built_effects import *

__all__ = ["PLAYER_MOVES", "MONSTER_MOVES"]

MONSTER_MOVES = {}
PLAYER_MOVES = {}
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




# PLAYER MOVE SEGMENT

# TESTED and WORKS
PLAYER_MOVES["attack"] = Move("attack",
    "image/icon/attack_icon.png",
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
        ScaleLevel(1),
        ScaleCritDamage(2)
        ])
    ])

# TESTED AND WORKS
PLAYER_MOVES["magic bolt"] = Move("magic bolt",
    "image/icon/magic_bolt_icon.png",
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

# TESTED AND WORKS
PLAYER_MOVES["blessing"] = Move("blessing",
    "image/icon/blessing_icon.png",
    [
    TargetOneOnly(),
    SingleTarget(),
    AlliesOnly(),
    AddEffect(StatChange("blessing", 5, "attack", 6))
    ])

# TESTED AND WORKS
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
        ScaleLevel(0.8)
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
        ScaleStat(1, "attack"),
        ScaleLevel(1),
        ScaleCritDamage(2)
        ])
    ])

# TESTED AND WORKS
PLAYER_MOVES["quick attack"] = Move("quick attack",
    "image/icon/quick_attack_icon.png",
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
        ScaleCritDamage(2)
        ])
    ])

# TESTED AND WORKS
PLAYER_MOVES["firebolt"] = Move("firebolt",
    "image/icon/firebolt_icon.png",
    [
    TargetOneOnly(),
    SingleTarget(),
    EnemiesOnly(),
    Damage(0, "magic",
        [
        ScaleStat(1, "magic"),
        ScaleLevel(0.6)
        ])
    ],
    crit_bound = 50,
    crit_components = [
    TargetOneOnly(),
    SingleTarget(),
    EnemiesOnly(),
    AddEffect(DoT("burning", 2, 5, 1, [ScaleLevelAdd(1)], "physical")),
    Damage(0, "magic",
        [
        ScaleStat(1, "magic"),
        ScaleLevel(0.6)
        ])
    ])

# TESTED AND WORKS
PLAYER_MOVES["arcane blast"] = Move("arcane blast",
    "image/icon/magic_blast_icon.png",
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

# TESTED AND WORKS
PLAYER_MOVES["healing word"] = Move("healing word",
    None,
    [
    TargetOneOnly(),
    SingleTarget(),
    Heal(10, [
        ScaleLevel(1)
        ])
    ])

# TESTED AND WORKS
PLAYER_MOVES["mark for death"] = Move("mark for death",
    None,
    [
    TargetOneOnly(),
    SingleTarget(),
    EnemiesOnly(),
    AddEffect(StatChange("marked", -5, "defense", 10))
    ])

# TESTED AND WORKS
PLAYER_MOVES["bolster"] = Move("bolster",
    None,
    [
    SelfTarget(),
    SelfEffect(StatChange("bolstered", 20, "defense", 8))
    ])

# DOESN'T WORK - CRASHES
# PLAYER_MOVES["cleave"] = Move("cleave",
#     None,
#     [
#     TargetNumberOnly(2),
#     EnemiesOnly(),
#     Damage(0, "physical",
#         [
#         ScaleStat(1, "attack"),
#         ScaleLevel(0.6),
#         ])
#     ],
#     crit_bound = 90,
#     crit_components = [
#     TargetOneOnly(),
#     SingleTarget(),
#     EnemiesOnly(),
#     Damage(0, "physical",
#         [
#         ScaleStat(1, "attack"),
#         ScaleLevel(0.6),
#         ScaleCritDamage(2)
#         ])
#     ])

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

# WORKS? Tho the double attack is not explicit
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
    Repeat(2,
        Damage(0, "physical",
            [
            ScaleStat(2, "attack"),
            ScaleLevel(0.6),
            ScaleCritDamage(2),
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