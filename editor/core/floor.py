from engine.serialization.serialization import deserialize

class FloorHandler:

    FLOORS = None

    def __init__(self):
        if not self.FLOORS:
            self.FLOORS = deserialize("data/scenario.p")

    def floors(self):
        return self.FLOORS