import time

import engine.game.move.built_moves as moves
from engine.game.character.character import Character
from engine.game.player.player import Player
from engine.game.monster.monster import Monster

players = []
george = Player("George")
fred = Player("Fred")
steve = Player("Steve")
george.add_move(moves.punch)
fred.add_move(moves.punch)
steve.add_move(moves.punch)
players.append(george)
players.append(fred)
players.append(steve)

monsters = []
mob1 = Monster()
mob2 = Monster()
mob3 = Monster()
monsters.append(mob1)
monsters.append(mob2)
monsters.append(mob3)

characters = list(players)
characters.extend(monsters)

delta = 0
cur_time = 0
prev_time = time.time()

monsters_dead = False
while not monsters_dead:
    cur_time = time.time()
    delta = cur_time - prev_time
    for char in characters:
        char.handle_battle(delta)
    prev_time = cur_time
    for player in players:
        if player.ready:
            print(player.name + " is ready!")
            valid_move = False
            while not valid_move:
                s = input()
                for move in player.moves:
                    if s == move.name:
                        mv = move
                        valid_move = True
            valid_target = False
            print("Select a target!")
            for monster in monsters:
                print(monster.name)
            while not valid_target:
                s = input()
                for monster in monsters:
                    if s == monster.name:
                        targ = monster
                        valid_target = True
            mv.cast(targ, player, players, monsters)
            player.action = 0
            cur_time = 0
            prev_time = time.time()

    monsters_dead = True
    for monster in monsters:
        if monster.fallen == False:
            monsters_dead = False