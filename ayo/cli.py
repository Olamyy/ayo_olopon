# -*- coding: utf-8 -*-

"""Console script for ayo."""

from match import Match
from .player import Human
from profiles import VectorAI
from config import MessageConfig, AyoConfig

from ayo.settings import BoardConfig

from termcolor import colored
from art import text2art
from tqdm import tqdm
import click


@click.command()
@click.option('--type', default="hvh", help=MessageConfig.GAME_TYPE, type=click.Choice(['hvh', 'hvc', 'cvc']))
@click.option('--pim', default=False, help=MessageConfig.PENALIZE_INVALID_MOVE)
@click.option('--pits', default=6, help=MessageConfig.DEFAULT_PITS)
@click.option('--stones', default=4, help=MessageConfig.DEFAULT_STONES)
def setup(type, pim, pits, stones):
    """Entry Point"""

    pbar = tqdm(range(10000))
    for char in pbar:
        pbar.set_description("INITIALIZING GAME %s" % char)
    print()

    print(colored("Setting up game with the following config: \n Game Type: {0} \n Board Pits: {1} \n Board Stones: {2} \n Penalize Invalid Moves: {3}".format(AyoConfig.GAME_TYPE_MAP.get(type), pits,
                                                                                                                                                               stones, pits), "yellow"))
    if click.confirm('Do you want to continue with this configuration?', abort=True):
        print(text2art("AYO \t \t \t \t OLOPON"))

    if type == "hvh":
        player_one_name = click.prompt("Enter a name for Player 1 : ")
        player_one = Human(name=player_one_name, pits=BoardConfig.PLAYER_ONE_PITS, store=BoardConfig.PLAYER_ONE_STORE)


        game = Match(player_one=HumanPlayer, player_two=HumanPlayer)
    elif type == "hvc":
        game = Match(player_one=HumanPlayer, player_two=VectorAI)
    else:
        game = Match(player_one=VectorAI, player_two=VectorAI)

    game.handle_next_move()


if __name__ == '__main__':
    setup()
