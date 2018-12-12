# -*- coding: utf-8 -*-

from ayo.board import Board
from ayo.player import Human
from ayo.exceptions import InvalidMoveError

from termcolor import colored


class Game(object):
    """ A match of Ayo has two Players and a Board.

    Match tracks current turn.

    """

    def __init__(self, players, board, **rules):
        """ Initializes a new match. """
        assert isinstance(board, Board), "The game board is not a valid board type"
        self.board = Board(**rules)
        self.player_one, self.player_two = players[0], players[1]
        self.starting_player = self.player_one if rules.get('start') == 1 else self.player_two

    def move(self):
        """
        Show board and move
        :return:
        """
        self.board.show_board()
        current_player = self.starting_player

        next_move = self.starting_player.play()
        try:
            self.board.board, free_move_earned = self.board.move_stones(current_player, next_move)
        except InvalidMoveError:
            if self._check_for_winner():
                import sys
                sys.exit()
            if current_player.__class__ == Human:
                print(colored('Please select a move with stones you can move.', 'red'))
            self.move()

    def _check_for_winner(self):
        pass
