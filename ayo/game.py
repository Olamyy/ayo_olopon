# -*- coding: utf-8 -*-
import sys

from board import Board
from player import Human
from utils import save_to_file_json
import datetime
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
        self.data_map = {self.player_one.id: {'moves': [], 'earned_free_move': [], 'won': [], 'invalid': [], 'points': [0]},
                         self.player_two.id: {'moves': [], 'earned_free_move': [], 'won': [], 'invalid': [], 'points': [0]},
                         'date': str(datetime.datetime.now())}
        self.rules = rules

    def move(self, player):
        """
        Show board and move
        :return:
        """

        current_player = player

        self.board.show_board()

        next_move = current_player.play(board=self.board, name=current_player.name, player=current_player, opponent=self.player_two if current_player == self.player_one else self.player_one)
        self.data_map[current_player.id]['moves'].append(next_move + 1)
        self.board.board, free_move_earned, invalid_move = self.board.move_stones(current_player, next_move)
        if invalid_move:
            self.data_map[current_player.id]['invalid'].append(1)
            if self.check_for_winner(current_player=current_player):
                self.data_map[current_player.id]['won'].append(1)
                self.data_map[self.player_one.id]['points'].append(self.get_score(self.player_one))
                self.data_map[self.player_two.id]['points'].append(self.get_score(self.player_two))
                save_to_file_json(self.data_map)
                sys.exit()
            else:
                self.data_map[current_player.id]['won'].append(0)
                if current_player.__class__ == Human:
                    print(colored('Please select a move with stones you can move.', 'red'))
                self.move(current_player)
                if self.rules.get('pim'):
                    sys.exit()
        self.data_map[current_player.id]['invalid'].append(0)
        if self.check_for_winner(current_player=current_player):
            self.data_map[current_player.id]['won'].append(1)
            self.data_map[self.player_one.id]['points'].append(self.get_score(self.player_one))
            self.data_map[self.player_two.id]['points'].append(self.get_score(self.player_two))
            save_to_file_json(self.data_map)
            sys.exit()
        self.data_map[current_player.id]['won'].append(0)
        if free_move_earned:
            self.data_map[current_player.id]['earned_free_move'].append(free_move_earned)
            self.move(current_player)
        else:
            current_player = self.swap_current_player(current_player)
            self.move(current_player)

    def get_score(self, player):
        board = self.board.gather_remaining(player)
        return board[player.store][0]

    def check_for_winner(self, **kwargs):
        player = kwargs.get('current_player')
        if set(self.board.board[player.pits]) == {0}:
            board = self.board.gather_remaining(player)
            print("Game Finished! \n  %s: %d | %s: %d" % (self.player_one.name, board[self.player_one.store][0], self.player_two.name, board[self.player_two.store][0]))
            return True
        else:
            return False

    def swap_current_player(self, current_player):
        if current_player == self.player_one:
            return self.player_two
        return self.player_one
