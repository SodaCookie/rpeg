import pickle

def serialize(obj, filename):
        pickle.dump(obj, open(filename, "wb"))

def deserialize(filename):
        return pickle.load(open(filename, "rb"))
