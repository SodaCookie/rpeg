"""Defines the Action class used by Dialogues"""

class Action(object):
    """Object used to run actions after a dialogue branch"""

    def execute(self, game):
        """Method to be called to execute after a dialogue branch
        has finished executing. Defaults to doing nothing. Meant
        to be subclassed and overridden."""
        pass