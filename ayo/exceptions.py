class InvalidBoardAreaError(Exception):
    """ Exception flagged when moves are attempted on an unknown area. """
    pass


class InvalidMoveError(Exception):
    """ Exception flagged when no stones are available at given index. """
    pass

