import pygame

from engine.system import Message
from engine.ui.element.abstractbutton import AbstractButton

class AbstractSlot(AbstractButton):
    """Generic slot element that holds some value of type item or move.
    Once instantiated, the slot is immutable in type. Does not
    handle the movement of the data! Only displays."""

    def __init__(self, name, rect, stype, address, cloneable=False,
            dropable=False, swapable=False):
        """Type of button used to transfer objects between "addresses"
        where the address is defined as a tuple of (container, key).
        cloneable indicates if the object will be cloned on pick up
        and dropable defines if the object can be thrown away if no slot
        accepts the object. stype defines the slot type. Only slots of
        the same time should interact with each other"""
        super().__init__(name, rect)
        self.stype = stype
        self.address = address # Memory location
        self.value = address[0][address[1]] # info used to draw
        self.cloneable = cloneable
        self.dropable = dropable
        self.swapable = swapable

    def on_drop(self, obj):
        """Override. Called whenever drop is invoked. Returns True to
        indicated that the drop is valid. False to indicate that it is not."""
        return True

    def on_change(self, value):
        """Override. Called whenever memory location is updated through
        set_address"""
        pass

    def set_address(self, value):
        """Set the controlled memory location"""
        self.address[0][self.address[1]] = value
        self.set_value(value)
        self.on_change(value)

    def set_value(self, value):
        self.value = value
        self.set_dirty(True)

    def on_click(self, game, system):
        """When clicked on will send a message to the hover system and
        determine if self needs to be set"""
        if self.value is not None:
            system.message("hover", Message("set", self.address, self,
                self.stype))
            if not self.cloneable:
                self.set_value(None)
                self.set_dirty(True)

    def off_click(self, game, system):
        """This off_click needs to be validated by the validator the the
        object will be dropped off"""
        if game.hover_data is not None:
            address, _, stype = game.hover_data
            other_container, other_key = address
            value = other_container[other_key]
            if stype == self.stype and self.on_drop(value):
                self.set_value(value)
                system.message("hover", Message("drop", self))

