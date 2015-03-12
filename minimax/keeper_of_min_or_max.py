"""
This module defines `KeeperOfMinOrMax` class. See its documentation.
"""

class KeeperOfMinOrMax:
    """
    Allows to keep min or max value in the values under consideration.
    Simple helper to avoid some conditional logic.

    Example usage:

    keeper = KeeperOfMinOrMax.max()

    keeper.value() # return None
    keeper.payload() # return None

    keeper.check_keep_or_reject(1, "payload1")
    keeper.check_keep_or_reject(3, "payload3")
    keeper.check_keep_or_reject(2) # you can omit payload

    keeper.value() # returns 3
    keeper.payload() # returns "payload3" string.

    # KeeperOfMinOrMax.min works in the same way

    """

    @staticmethod
    def max():
        """returns an instance for tracking max value"""
        return KeeperOfMinOrMax(int.__lt__)

    @staticmethod
    def min():
        """returns an instance for tracking min value"""
        return KeeperOfMinOrMax(int.__gt__)

    def __init__(self, comp_method):
        self._comp_method = comp_method
        self._value = None
        self._payload = None

    def check_keep_or_reject(self, value, payload=None):
        """performs comparison and saves the value and payload if the value is
        the value is greater or less that already stored"""
        if self._value == None:
            self._value = value
            self._payload = payload
            return

        if self._comp_method(self._value, value):
            self._value = value
            self._payload = payload

    def value(self):
        """value getter"""
        return self._value

    def payload(self):
        """payload getter"""
        return self._payload
