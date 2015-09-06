"""Implements the interface required to bind to a zone"""

class Bindable(object):
    """Simple interface for binding to a Zone object
    the bindable interface only implements the bind method
    and adds a attribute called bound"""

    def __init__(self):
        self.bound = None

    def bind(self, zone):
        """Binds object to zone object"""
        self.bound = zone