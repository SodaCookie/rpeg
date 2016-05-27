import dill as pickle

def serialize(obj, filename):
    with open(filename, "wb") as file:
        pickle.dump(obj, file)

def deserialize(filename):
    with open(filename, "rb") as file:
        return pickle.load(file)
