from settings import BoardConfig
from board import Board
import random
import math


class Player(object):
    """ A game player """

    def __init__(self, name, pits, store, points=0):
        self.name = name
        self.id = self.generate_id()
        self.points = points
        self.pits = pits
        self.store = store

    def generate_id(self):
        import uuid
        id_ = str(uuid.uuid4()).replace('-', '')
        return id_[:5]


class Human(Player):
    def play(self, **kwargs):
        """ Get a human player's next move """
        value = input("Please input your next move (1 to {}): ".format(BoardConfig.MAX_PITS))
        return int(value) - 1


class Computer(Player):

    def get_pits(self, board):
        """ Shortcut to AI pits. """
        return board[self.pits]

    def eligible_moves(self, board):
        """ Returns a list of integers representing eligible moves. """
        eligible_moves = []
        for i in range(len(self.get_pits(board))):
            if not self.get_pits(board)[i] == 0:
                eligible_moves.append(i)
        return eligible_moves

    def eligible_free_turns(self, board):
        """ Returns a list of indexes representing eligible free turns. """

        free_turn_indices = list(reversed(range(1, 7)))
        elig_free_turns = []

        for i in range(0, 6):
            if self.get_pits(board)[i] == free_turn_indices[i]:
                elig_free_turns.append(1)
            else:
                elig_free_turns.append(0)

        return elig_free_turns

    def think(self, player):
        """ Slight delay for thinking. """
        import time
        from termcolor import colored
        print(colored('{} is thinking...', 'green').format(player))
        time.sleep(3)


class RandomPlayer(Computer):
    def play(self, board=None, name=None):
        # self.think(self.name)  @Todo : Fix
        self.think(name)
        return random.choice(self.eligible_moves(board))


class MiniMaxPlayer(Computer):
    def play(self, **kwargs):
        pass


class GreedyPlayer(Computer):
    """
    A simple implementation of the greedy algorithm.
    """

    def play(self, **kwargs):
        self.think(self.name)
        board, player, opponent = kwargs.get('board'), kwargs.get('player'), kwargs.get('opponent')
        board_list = board.board
        best = - math.inf
        greedy_move = 0
        eligible_moves = self.eligible_moves(board_list)
        for move in eligible_moves:
            if self.evaluate_move(move, board, player=player, opponent=opponent) >= best:
                best = self.evaluate_move(move, board, player=player, opponent=opponent)
                greedy_move = move
        return greedy_move

    def evaluate_move(self, move, board, **kwargs):
        current_player, opponent = kwargs.get('player'), kwargs.get('opponent')
        board.move_stones(current_player, move)
        return current_player.store - opponent.store


class VectorPlayer(Computer):
    def play(self, **kwargs):
        board = kwargs.get('board').board
        """ Use an reverse indices vector to optimize for free turns. """
        self.think(self.name)

        all_moves = list(reversed(range(0, 6)))
        all_moves.reverse()

        for i in all_moves:
            if self.eligible_free_turns(board)[i] == 1:
                if self.get_pits(board)[i] == Board.reverse_index(i) + 1:
                    return i
        for i in all_moves:
            if self.get_pits(board)[i] > Board.reverse_index(i) + 1:
                return i
        return random.choice(self.eligible_moves(board))
