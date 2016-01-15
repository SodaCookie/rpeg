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
    "",
    None,
    [
    TargetOneOnly(),
    SingleCast(),
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
    SingleCast(),
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
    "",
    None,
    [
    TargetOneOnly(),
    SingleCast(),
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
    "",
    None,
    [
    TargetOneOnly(),
    SingleCast(),
    AlliesOnly(),
    AddEffect(StatChange("blessing", 5, "attack", 6))
    ])

# TESTED AND WORKS
PLAYER_MOVES["stunning blow"] = Move("stunning blow",
    None,
    "",
    None,
    [
    TargetOneOnly(),
    SingleCast(),
    EnemiesOnly(),
    AddChanceEffect(Stun(5), 1),
    Damage(0, "physical",
        [
        ScaleStat(1, "attack"),
        ScaleLevel(0.8)
        ])
    ],
    crit_bound = 90,
    crit_components = [
    TargetOneOnly(),
    SingleCast(),
    EnemiesOnly(),
    AddChanceEffect(Stun(5), 1),
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
    "",
    None,
    [
    TargetOneOnly(),
    SingleCast(),
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
    SingleCast(),
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
    "",
    None,
    [
    TargetOneOnly(),
    SingleCast(),
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
    SingleCast(),
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
    "",
    None,
    [
    TargetOneOnly(),
    GroupCast(),
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
    "",
    None,
    [
    TargetOneOnly(),
    SingleCast(),
    Heal(10, [
        ScaleLevel(1)
        ])
    ])

# TESTED AND WORKS
PLAYER_MOVES["mark for death"] = Move("mark for death",
    None,
    "",
    None,
    [
    TargetOneOnly(),
    SingleCast(),
    EnemiesOnly(),
    AddEffect(StatChange("marked", -5, "defense", 10))
    ])

# TESTED AND WORKS
PLAYER_MOVES["bolster"] = Move("bolster",
    None,
    "",
    None,
    [
    SelfCast(),
    SelfEffect(StatChange("bolstered", 20, "defense", 8))
    ])

# TESTED AND WORKS
PLAYER_MOVES["cleave"] = Move("cleave",
    None,
    "",
    None,
    [
    SingleCast(),
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
    SingleCast(),
    EnemiesOnly(),
    Damage(0, "physical",
        [
        ScaleStat(1, "attack"),
        ScaleLevel(0.6),
        ScaleCritDamage(2)
        ])
    ])

# IGNORES DEFENSE OF STUNNED TARGET
PLAYER_MOVES["backstab"] = Move("backstab",
    None,
    "",
    None,
    [
    TargetOneOnly(),
    SingleCast(),
    EnemiesOnly(),
    Conditional(
        lambda target, caster, players, monsters: target.has_effect("stunned"),
        [Damage(0, "true",
            [
            ScaleStat(1, "attack"),
            ScaleLevel(1),
            ])],
        [Damage(0, "physical",
            [
            ScaleStat(1, "attack"),
            ScaleLevel(1),
            ])]
    )],
    crit_bound = 90,
    crit_components = [
    TargetOneOnly(),
    SingleCast(),
    EnemiesOnly(),
    Conditional(
        lambda target, caster, players, monsters: target.has_effect("stunned"),
        [Damage(0, "true",
            [
            ScaleStat(1, "attack"),
            ScaleLevel(1),
            ScaleCritDamage(3),
            ])],
        [Damage(0, "physical",
            [
            ScaleStat(1, "attack"),
            ScaleLevel(1),
            ScaleCritDamage(3),
            ])])
    ])

# WORKS? Tho the double attack is not explicit
PLAYER_MOVES["double stab"] = Move("double stab",
    None,
    "",
    None,
    [
    TargetOneOnly(),
    SingleCast(),
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
    SingleCast(),
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

# Standard physical attack
MONSTER_MOVES["attack"] = Move("attack",
    None,
    "",
    None,
    [
    RandomEnemyCast(),
    EnemiesOnly(),
    Damage(0, "physical",
        [
        ScaleStat(1, "attack"),
        ])
    ])

# Rat standard physical attack
MONSTER_MOVES["bite"] = Move("bite",
    None,
    "",
    None,
    [
    RandomEnemyCast(),
    EnemiesOnly(),
    Damage(0, "physical",
        [
        ScaleStat(1, "attack"),
        ])
    ])

# Plagued rat physical attack
MONSTER_MOVES["plagued bite"] = Move("plagued bite",
    None,
    "",
    None,
    [
    RandomEnemyCast(),
    EnemiesOnly(),
    AddEffect(StatChange("diseased", -3, "attack", 5)),
    Damage(0, "physical",
        [
        ScaleStat(1, "attack"),
        ])
    ])

# Spider standard attack
MONSTER_MOVES["venomous bite"] = Move("venomous bite",
    None,
    "",
    None,
    [
    RandomEnemyCast(),
    EnemiesOnly(),
    AddEffect(DoT("poisoned", 5, 5, 1, None, "magic")),
    Damage(0, "physical",
        [
        ScaleStat(1, "attack"),
        ])
    ])

# Spider debuff attack
MONSTER_MOVES["web wrap"] = Move("web wrap",
    None,
    "",
    None,
    [
    RandomEnemyCast(),
    EnemiesOnly(),
    AddEffect(StatChange("wrapped", -5, "speed", 5))
    ])

# Lost soul standard AoE magic attack
MONSTER_MOVES["piercing shriek"] = Move("piercing shriek",
    None,
    "",
    None,
    [
    GroupCast(),
    EnemiesOnly(),
    Damage(0, "magic",
        [
        ScaleStat(0.7, "magic"),
        ])
    ])

# Lost soul single target nuke/heal
MONSTER_MOVES["soul drain"] = Move("soul drain",
    None,
    "",
    None,
    [
    RandomEnemyCast(),
    SelfCast(),
    EnemiesOnly(),
    Conditional(
        lambda target, caster, players, monsters: target.is_enemy(),
        [Damage(0, "magic",
        [
        ScaleStat(1, "magic"),
        ])],
        Heal(0,
        [
        ScaleStat(1, "magic"),
        ]))
    ])

# Zombie special attack
MONSTER_MOVES["festering bite"] = Move("festering bite",
    None,
    "",
    None,
    [
    RandomEnemyCast(),
    EnemiesOnly(),
    AddEffect(StatChange("open wound", -3, "defense", 5)),
    Damage(0, "physical",
        [
        ScaleStat(1, "attack"),
        ])
    ])

# AoE physical attack for abomination
MONSTER_MOVES["cleave"] = Move("cleave",
    None,
    "",
    None,
    [
    GroupCast(),
    EnemiesOnly(),
    Damage(0, "physical",
        [
        ScaleStat(0.7, "physical"),
        ])
    ])

# Magic Damage DoT for necromancer
MONSTER_MOVES["decay"] = Move("decay",
    None,
    "",
    None,
    [
    RandomEnemyCast(),
    EnemiesOnly(),
    AddEffect(DoT("decaying", 5, 7, 1, None, "magic")),
    ])

# Necromancer AoE Debuff
MONSTER_MOVES["plague"] = Move("plague",
    None,
    "",
    None,
    [
    GroupCast(),
    EnemiesOnly(),
    AddEffect(StatChange("diseased", -5, "attack", 5))
    ])

# AoE physical attack for the necromancer
MONSTER_MOVES["hands of the dead"] = Move("hands of the dead",
    None,
    "",
    None,
    [
    GroupCast(),
    EnemiesOnly(),
    Damage(0, "physical",
        [
        ScaleStat(0.7, "physical"),
        ])
    ])

# Summon minions move for necromancer