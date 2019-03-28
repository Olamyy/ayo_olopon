# -*- coding: utf-8 -*-

"""Console script for ayo."""

from board import Board
from game import Game
from player import Human, VectorPlayer, RandomPlayer, GreedyPlayer
from settings import MessageConfig, BoardConfig
from utils import generate_name
from termcolor import colored
from art import text2art
from tqdm import tqdm
import click


@click.command()
@click.option('--game', default="hvh", help=MessageConfig.GAME_TYPE, type=click.Choice(['hvh', 'hvc', 'cvc']))
@click.option('--pim', default=False, help=MessageConfig.PENALIZE_INVALID_MOVE)
@click.option('--pits', default=6, help=MessageConfig.DEFAULT_PITS)
@click.option('--stones', default=4, help=MessageConfig.DEFAULT_STONES)
@click.option('--config', type=click.Path(), help="Config File")
def setup(game, pim, pits, stones, config=None):
    """Entry Point"""

    pbar = tqdm(range(10000))
    for char in pbar:
        pbar.set_description("INITIALIZING GAME %s" % char)
    print()

    if config:
        pbar = tqdm(range(10000))
        for _ in pbar:
            pbar.set_description("GETTING CONFIGURATION FROM {0}".format(config))
        print()
        import yaml
        with open(config, 'r') as stream:
            try:
                config_dict = yaml.load(stream)['config']
                pim, pits, stones = config_dict.get('pim', pim), config_dict.get('pits', pits), config_dict.get('stones', stones)
                game = config_dict.get('game', game)
            except yaml.YAMLError as exc:
                print("Something went wrong with reading your config file. \n {}".format(exc))

    print(colored("Setting up game with the following config: \n Game Type: {0} "
                  "\n Board Pits: {1} \n Board Stones: {2} \n Penalize Invalid Moves: {3}"
                  .format(BoardConfig.GAME_TYPE_MAP.get(game), pits, stones, pim), "yellow"))
    print()
    if click.confirm('Do you want to continue with this configuration?', abort=True):
        print(text2art("AYO \t \t \t \t OLOPON"))

    board = Board(pim=pim, pits=pits, stones=stones)

    if game == "hvh":
        player_one_name, player_two_name = click.prompt("Enter a name for Player 1 "), click.prompt("Enter a name for Player 2 ")
        player_one = Human(name=player_one_name, pits=BoardConfig.PLAYER_ONE_PITS, store=BoardConfig.PLAYER_ONE_STORE)
        player_two = Human(name=player_two_name, pits=BoardConfig.PLAYER_TWO_PITS, store=BoardConfig.PLAYER_TWO_STORE)
        game = Game(players=[player_one, player_two], board=board)
    elif game == "hvc":
        player_one_name = click.prompt("Enter a name for the human player")
        player_one = Human(name=player_one_name, pits=BoardConfig.PLAYER_ONE_PITS, store=BoardConfig.PLAYER_ONE_STORE)
        player_two = VectorPlayer(name=generate_name(), pits=BoardConfig.PLAYER_TWO_PITS, store=BoardConfig.PLAYER_TWO_STORE)
        game = Game(players=[player_one, player_two], board=board)
    else:
        player_one = VectorPlayer(name=generate_name(), pits=BoardConfig.PLAYER_ONE_PITS, store=BoardConfig.PLAYER_ONE_STORE)
        player_two = VectorPlayer(name=generate_name(), pits=BoardConfig.PLAYER_TWO_PITS, store=BoardConfig.PLAYER_TWO_STORE)
        game = Game(players=[player_one, player_two], board=board)

    if click.confirm('\n\n{} vs {}. \n Start Game'.format(player_one.name.upper(), player_two.name.upper()), abort=True):
        game.move(player_one)


if __name__ == '__main__':
    setup()
