from ayo.settings import BoardConfig


class Player(object):
    """ A game player """

    def __init__(self, name, pits, store,  board=None, points=0):
        self.name = name
        self.board = board
        self.id = self.generate_id()
        self.points = points
        self.pits = pits
        self.store = store

    def generate_id(self):
        import uuid
        return str(uuid.uuid4()).replace('-', '')


class Human(Player):
    def __init__(self, name, pits, store,  board=None, points=0):
        super(Human, self).__init__(name, board, points)

    def play(self):
        """ Get a human player's next move """
        value = input("Please input your next move (1 to {}): ".format(BoardConfig.MAX_PITS))
        return int(value) - 1


class Computer(Player):
    def __init__(self, name, pits, store,  board=None, points=0):
        super(Computer, self).__init__(name, board, points)

    def pits(self):
        """ Shortcut to AI pits. """

