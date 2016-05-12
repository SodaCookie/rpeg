# rpeg
RPG engine written in Python with the use of the Pygame library.
Built to support easy development of roguelike games in the style of FTL.

Features a GUI editor implemented with PyQt5 to easily allow game development through the creation and insertion of game data.
Also features a programmatic interface to allow developers to extend the game through Python scripting.

# In Development
Main engine is developed.
Editor interfarce is currently in development.

# Examples
The GUI editor being used to create an event in the game

![alt text](https://github.com/SodaCookie/RPG-Game/blob/master/image/example/exampleGui.png)

An example of scripting used to extended a character move component

```Python
class RandomAllyCast(Component):
    """Defines Random Ally Target for a move"""
    def get_targets(self, selected, caster, players, monsters):
        if isinstance(type(caster), type(players[0])):
            return [random.choice([player for player in players if \
                not player.fallen])]
        return [random.choice([monster for monster in monsters if \
            not monster.fallen])]
```
