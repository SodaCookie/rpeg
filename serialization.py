import dill as pickle

from engine.game.move.built_moves import MOVES
from engine.game.monster.monster import Monster

def serialize(obj, filename):
        pickle.dump(obj, open(filename, "wb"))

def deserialize(filename):
        return pickle.load(open(filename, "rb"))

if __name__ == "__main__":
    # path = "data/item/base/"
    # for key in built_items.BASE_ITEMS.keys():
    #     qual_path = path + key.replace(" ", "_") + ".p"
    #     serialize(built_items.BASE_ITEMS[key], qual_path)
    # path = "data/item/"
    # for key in built_items.ITEMS.keys():
    #     qual_path = path + key.replace(" ", "_") + ".p"
    #     serialize(built_items.ITEMS[key], qual_path)
    serialize(Monster.MONSTERS, "data/monster.p")
