'''
This module defines `BoxWalker` class. See its documentation.
'''

class BoxWalker:
    """This class allows to iterate through adjacent elements in
    two-dimensional arrays of data, in horizontal, vertical or diagonal
    directions.
    It can help to detect sequences of identical elements in 2d arrays.
    For example: we have a 2d array of tictactoe game state (with "x" and
    "o" elemenets), and we know that the last move was made by the "x" player
    to the (0, 0) cell. So we can check if the user is a winner, without
    checking all vertical, horizontal and diagonal sequences. We can walk
    from the cell (0, 0) to the right, down, and diagonally to the right-down.
    It's cheaper than go through all the cells. This is especially beneficial
    for large arrays, and can be uses as a good optimization.

    Example usage:

    ary - 2d array of chars (" ", "x" or "o")
    field_width = 3
    field_height = 3
    last_step_x = 1
    last_step_y = 1

    walker = BoxWalker(field_width, field_height, last_step_x, last_step_y)

    # checking horizontal cells

    count = 0
    # This method will iterate us on all available steps in the specified
    # direction, within the specified borders.
    # It iterates only on adjacent cells, so we can count the continuous
    # sequence.
    for x, y in walker.steps_in_direction(1, 0):
        if ary[x][y] == "x":
            count += 1
            if count == 3:
                # We found a continuous sequence of three "x" chars.
                # So we found the winner.
                break
        else:
            # Here we decide that further sequence is broken (we found chars
            # other than "x") and we want to try the opposite direction.
            # This 
            walker.turn_around_or_stop()

    """

    def __init__(self, width, height, pos_x, pos_y):
        self._width = width
        self._height = height
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._stopped = False

        if self._is_out_of_the_box(self._pos_x, self._pos_y):
            raise ValueError("pos_x and pos_y should be inside the box " \
                    "(width: %d, height: %d, x: %d, y: %d)" % \
                    (self._width, self._height, self._pos_x, self._pos_y))

    def _is_out_of_the_box(self, pos_x, pos_y):
        """Checks if provided x,y coordinats belongs to the area inside the
            box"""

        if pos_x < 0 or pos_x >= self._width:
            return True

        if pos_y < 0 or pos_y >= self._height:
            return True

        return False

    def steps_in_direction(self, dir_x, dir_y):
        """Returns generator. Iterates on all available steps within the
        specified box.
        dir_x and dir_y arguments can indicate only vertical, horizontal or
        diagonal direction. So their values can be only -1, 0 or 1.
        """
        for direction in [dir_x, dir_y]:
            if direction not in (-1, 0, 1):
                raise ValueError("dir_x and dir_y can be only -1, 0, 1, " \
                        "but %d provided" % direction)

        if dir_x == 0 and dir_y == 0:
            raise ValueError("dir_x and dir_y can't be 0 at the same time")

        yield self._pos_x, self._pos_y

        for positive_or_negative in [1, -1]:
            self._stopped = False

            dir_x *= positive_or_negative
            dir_y *= positive_or_negative

            inc_x = dir_x
            inc_y = dir_y

            while True:
                if self._stopped:
                    break

                pos_x = self._pos_x + inc_x
                pos_y = self._pos_y + inc_y

                if self._is_out_of_the_box(pos_x, pos_y):
                    break

                yield pos_x, pos_y

                inc_x += dir_x
                inc_y += dir_y

    def turn_around_or_stop(self):
        """Indicates that we should turn around and iterate in reverse
        direction.
        """
        self._stopped = True
