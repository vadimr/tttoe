# pylint: disable=too-many-arguments, protected-access

"""
This module defines `GameState` class. See its documentation.
"""

import copy
from tttoe.boxwalker import BoxWalker

class GameState:
    """Stores a state of tictactoe game.
    `make_move` method allows to make the game move, and returns a new
    GameState instance as a result. The new instance stores the result of the
    previous move (move w/o win, draw or the winner sign).

    Example usage:

    field_width = 3
    field_hight = 3
    sequence_to_win = 3

    state = GameState(field_width, field_hight, sequence_to_win)

    new_state = state.make_move(0, 0, "x")
    new_state.last_move_result # returns "nothing", what indicates that the
                               # terminal state is not reached.

    new_state = new_state.make_move(1, 0, "x")
    new_state = new_state.make_move(2, 0, "x")

    new_state.last_move_result # returns "x", what means that the terminal
                               # state is reached, and "x" is a winner.
                               # See `last_move_result` doc.
    """

    def __init__(self, width, height, qty_to_win, field=None):
        self._width = width
        self._height = height
        self._qty_to_win = qty_to_win
        self._last_move_result = "nothing"

        if field == None:
            self._field = [[None for _ in range(self._height) ] for _ in range(self._width)]
        else:
            self._field = copy.deepcopy(field)

    @property
    def field(self):
        return self._field

    def _is_fully_filled(self):
        for _ in self.all_available_moves():
            return False
        return True

    def _clone(self):
        return GameState(self._width, self._height, self._qty_to_win, \
            field=self._field)

    def all_available_moves(self):
        """Generator on each possible move that can be perfoemed. Yields x and
        y positions of possible steps."""
        for x in range(self._width):
            for y in range(self._height):
                if self._field[x][y] == None:
                    yield x, y

    def make_move(self, pos_x, pos_y, player_handle):
        """Makes move and returns new state as a result. New state contains
        the result of previous move (see `last_move_result` method).

        Instead of scanning all field cells after each move, we use one
        optimization.
        As we know what was the last move position (x,y position),
        and the player's sign ("x", "o" or whatever), we can scan only the
        surrounding cells of the performed move, to detect if we have a "win"
        state. We just need to scan surrounding cells on the same row,
        same column and diagonals.
        For example, if the goal sequence to win equals 3, we need to scan
        these cells (x - the place of the last move)

        # # #
         ###
        ##x##
         ###
        # # #

        This optimization is very beneficial for large fields.

        `make_move` arguments:
            * pos_x, pos_y - the position of the cell to place a character
            * player_handle - handle of the player (usually "x" or "y" string
                if tictactoe). "nothing" and "draw" handles (strings) are
                reserved and used as result of `last_move_result` method.
        """

        if player_handle in ("nothing", "draw"):
            raise ValueError("\"nothing\" and \"draw\" hanles are reserved")

        if self._field[pos_x][pos_y] != None:
            raise ValueError("The value in the cell (%d, %d) is already set" % \
                    (pos_x, pos_y))

        new_state = self._clone()
        new_state._field[pos_x][pos_y] = player_handle

        walker = BoxWalker(new_state._width, new_state._height, pos_x, pos_y)

        for direction in [(1, 0), (0, 1), (1, 1), (1, -1)]:
            count = 0

            for x, y in walker.steps_in_direction(direction[0], direction[1]):
                if new_state._field[x][y] == player_handle:
                    count += 1
                    if count == new_state._qty_to_win:
                        new_state._last_move_result = player_handle
                        return new_state
                else:
                    walker.turn_around_or_stop()

        if new_state._is_fully_filled():
            new_state._last_move_result = "draw"
            return new_state

        new_state._last_move_result = "nothing"
        return new_state

    @property
    def last_move_result(self):
        """Returns the result of the previous move
        Possible values:
            * "nothing" - regular move, no winner, no draw
            * "draw" - draw, no moves can be done
            * any string which was used with `make_move` method. Means
            that the player who use this handle string is the winner.
        """
        return self._last_move_result
