"""Defines an abstract parser."""

class AbstractParser(object):
    """Defines the interface for Parsers"""

    def read(self, file):
        """Override this method to make the parser's read.
        An object that represents the data is expected to be returned."""
        pass

    def write(self, obj):
        """Override this method to make the parser's write.
        Given an object, the raw xml data is expected to be returned."""
        pass