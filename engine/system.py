"""Defines the System interface and Message class"""

class Message(object):
    """Simple class used to construct Message objects"""

    def __init__(self, mtype, *args):
        self.mtype = mtype
        self.args = args


class System(object):
    """Interface for creating a new system in the Game"""

    def __init__(self, game, name):
        """Initialize a new System"""
        super().__init__()
        self.queue = [] # Message queue
        self.game = game
        self.name = name

    def init(self, game):
        """Override. Called at the start of the game"""
        pass

    def update(self, delta, game):
        """Override. Called every game cycle"""
        pass

    def quit(self, game):
        """Override. Called at the end of the game"""
        pass

    def flush_messages(self):
        """Returns all the messages passed to the system"""
        old_queue = self.queue
        self.queue = []
        return old_queue

    def message(self, message):
        """Passes a message to the system"""
        self.queue.append(message)