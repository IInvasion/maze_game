"""Position utility."""


class Position:
    """Position."""

    def __init__(self, row_max, col_max):
        """Constructor."""
        self._row = 0
        self._col = 0
        self._row_max = row_max
        self._col_max = col_max

    def _clone(self, row=None, col=None):
        """Partially clone position."""
        pos = Position(self._row_max, self._col_max)
        new_row = row if row is not None else self._row
        new_col = col if col is not None else self._col
        pos.update(new_row, new_col)
        return pos

    def _valid_col(self, col):
        """Check if column is valid."""
        return 0 <= col < self._col_max

    def _valid_row(self, row):
        """Check if row is valid."""
        return 0 <= row < self._row_max

    def down(self):
        """Position to move down."""
        new_row = self._row + 1
        valid = self._valid_row(new_row)
        return self._clone(row=new_row) if valid else None

    def left(self):
        """Position to move left."""
        new_col = self._col - 1
        valid = self._valid_col(new_col)
        return self._clone(col=new_col) if valid else None

    def right(self):
        """Position to move right."""
        new_col = self._col + 1
        valid = self._valid_col(new_col)
        return self._clone(col=new_col) if valid else None

    def up(self):  # pylint: disable=invalid-name
        """Position to move up."""
        new_row = self._row - 1
        valid = self._valid_row(new_row)
        return self._clone(row=new_row) if valid else None

    def pair(self):
        """Return coordinate pair."""
        return (self._row, self._col)

    def update(self, row, col):
        """Update position."""
        self._row = row
        self._col = col
