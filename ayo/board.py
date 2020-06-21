# -*- coding: utf-8 -*-

from ayo.settings import BoardConfig
from ayo.exceptions import InvalidBoardAreaError, InvalidMoveError
from termcolor import colored
import sys


class Board(object):
    """ An Ayo board with size pits and stones """

    def __init__(self, pits=None, stones=None, **rules):
        pits = pits if pits else BoardConfig.MAX_PITS
        stones = stones if stones else BoardConfig.MAX_STONES
        self.board = [[stones] * pits, [0], [stones] * pits, [0]]
        self.rules = rules

    def show_board(self):
        """ Returns the current board as a printable string to show the user.
            Note that the order of player 2 pits are displayed in reverse
            from the list index to give the appearance of a loop.
        """

        print("   %d  %d  %d  %d  %d  %d\n %d                   %d\n   %d  %d  %d  %d  %d  %d\n" % (
            # Player 2 pits in top row
            self.board[2][5], self.board[2][4], self.board[2][3],
            self.board[2][2], self.board[2][1], self.board[2][0],
            # Player 2 & 1 stores in middle row
            self.board[3][0], self.board[1][0],

            # Player 1 pits on bottom row
            self.board[0][0], self.board[0][1], self.board[0][2],
            self.board[0][3], self.board[0][4], self.board[0][5]))

    def move_stones(self, player, position):
        current_area = player.pits

        print("Current Area", current_area)

        print(self.board[current_area][position])

        if not self.board[current_area][position]:
            if self.rules.get("pim"):
                player.points -= 1
                print(colored(f'That move is not allowed. Penalizing {player.name}. Current point {player.points}',
                              'red'))
                print('Exiting Game')
                sys.exit(1)
            print(colored('Invalid Move. There are no stones to pick in this pit.', 'red'))
            return self.board, False, True

        stones_grabbed = self.board[current_area][position]
        self.board[current_area][position] = 0

        index = position

        for stones in range(stones_grabbed):
            try:
                self.board[current_area][index + 1] += 1
                index += 1
            except IndexError:
                current_area = self.get_next_area(current_area)
                index = 0
                self.board[current_area][index] += 1

        free_move = self.earned_free_move(player, current_area)

        if self.earned_capture(player, current_area, index):
            self.board = self.process_capture(player, current_area, index)

        return self.board, free_move, False

    def get_next_area(self, current_area):
        """ Given a current area of transaction, gives the next area. """
        if current_area == BoardConfig.PLAYER_ONE_PITS:
            return BoardConfig.PLAYER_ONE_STORE
        elif current_area == BoardConfig.PLAYER_ONE_STORE:
            return BoardConfig.PLAYER_TWO_PITS
        elif current_area == BoardConfig.PLAYER_TWO_PITS:
            return BoardConfig.PLAYER_TWO_STORE
        elif current_area == BoardConfig.PLAYER_TWO_STORE:
            return BoardConfig.PLAYER_TWO_PITS
        else:
            raise InvalidBoardAreaError

    def earned_free_move(self, player, last_area):
        if last_area == player.store:
            print(colored(f"{player.name} earned a free move!", "yellow"))
            return True
        return False

    def earned_capture(self, player, area, index):
        opposing_area, opposing_index = self.get_opposing_area_and_index(player, area, index)
        if player.pits != area:
            return False
        if self.board[area][index] > 1:
            return False
        elif self.board[opposing_area][opposing_index] == 0:
            return False
        else:
            return True

    def process_capture(self, player, area, index):
        """ Processes capture by moving stones to the player's store. """
        if player.pits == BoardConfig.PLAYER_ONE_PITS:
            destination_store = BoardConfig.PLAYER_ONE_STORE
        else:
            destination_store = BoardConfig.PLAYER_TWO_STORE

        opposing_area, opposing_index = self.get_opposing_area_and_index(player, area, index)
        captured_stones = self.board[opposing_area][opposing_index]
        print(f'{captured_stones} stones captured.')

        # Clear the two pits
        self.board[area][index] = 0
        self.board[opposing_area][opposing_index] = 0

        # Move captures and original stone to store
        total_gain = captured_stones + 1
        self.board[destination_store][0] += total_gain

        return self.board

    @classmethod
    def reverse_index(cls, index):
        """ Returns the mirror index to the one given. """
        rev_index = range(0, 6)
        rev_index = list(reversed(rev_index))
        return rev_index[index]

    def get_opposing_area_and_index(self, player, area, index):
        if area == player.pits:
            opposing_area = BoardConfig.PLAYER_TWO_PITS
        elif area != player.pits:
            opposing_area = BoardConfig.PLAYER_ONE_PITS
        elif area == BoardConfig.PLAYER_ONE_STORE:
            opposing_area = BoardConfig.PLAYER_TWO_STORE
        elif area == BoardConfig.PLAYER_TWO_STORE:
            opposing_area = BoardConfig.PLAYER_ONE_STORE
        else:
            raise InvalidBoardAreaError

        opposing_index = self.reverse_index(index)

        return opposing_area, opposing_index

    def gather_remaining(self, player):
        remaining_area = player.pits
        destination_store = player.store
        remaining_stones = 0
        for i in range(6):
            remaining_stones += self.board[remaining_area][i]
            self.board[remaining_area][i] = 0

        self.board[destination_store][0] += remaining_stones

        return self.board

