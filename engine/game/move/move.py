class Move(object):

    def __init__(self, name, components = None):
        self.name = name
        self.animation = NotImplemented
        if components != None:
            self.components = components
        else:
            self.components = []