# -*- coding: utf-8 -*-

"""Console script for ayo."""
import yaml
from yaml.loader import FullLoader
from termcolor import colored
from art import text2art
from tqdm import tqdm
import click

from ayo.board import Board
from ayo.exceptions import InvalidConfigError
from ayo.game import Game
from ayo.player import Human, VectorPlayer
from ayo.settings import MessageConfig, BoardConfig
from ayo.utils import generate_name


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
            pbar.set_description(f"GETTING CONFIGURATION FROM {config}")
        print()
        with open(config, 'r') as stream:
            try:
                config_dict = yaml.load(stream, Loader=FullLoader)['config']
                pim, pits, stones = config_dict.get('pim', pim), config_dict.get('pits', pits), config_dict.get(
                    'stones', stones)
                game = config_dict.get('game', game)
            except yaml.YAMLError as exc:
                raise InvalidConfigError(
                    f"Something went wrong while reading your config file. \n {exc}"
                )

    print(f"Setting up game with the following config: \n Game Type: {BoardConfig.GAME_TYPE_MAP.get(game)} \n Board "
          f"Pits: {pits} \n Board Stones: {stones} \n Penalize Invalid Moves: {pim}")

    print()
    if click.confirm('Do you want to continue with this configuration?', abort=True):
        print(text2art("AYO \t \t \t \t OLOPON"))

    board = Board(pim=pim, pits=pits, stones=stones)

    if game == "hvh":
        player_one_name, player_two_name = click.prompt("Enter a name for Player 1 "), click.prompt(
            "Enter a name for Player 2 ")
        player_one = Human(name=player_one_name, pits=BoardConfig.PLAYER_ONE_PITS, store=BoardConfig.PLAYER_ONE_STORE)
        player_two = Human(name=player_two_name, pits=BoardConfig.PLAYER_TWO_PITS, store=BoardConfig.PLAYER_TWO_STORE)
        game = Game(players=[player_one, player_two], board=board)
    elif game == "hvc":
        player_one_name = click.prompt("Enter a name for the human player")
        player_one = Human(name=player_one_name, pits=BoardConfig.PLAYER_ONE_PITS, store=BoardConfig.PLAYER_ONE_STORE)
        player_two = VectorPlayer(name=generate_name(), pits=BoardConfig.PLAYER_TWO_PITS,
                                  store=BoardConfig.PLAYER_TWO_STORE)
        game = Game(players=[player_one, player_two], board=board)
    else:
        player_one = VectorPlayer(name=generate_name(), pits=BoardConfig.PLAYER_ONE_PITS,
                                  store=BoardConfig.PLAYER_ONE_STORE)
        player_two = VectorPlayer(name=generate_name(), pits=BoardConfig.PLAYER_TWO_PITS,
                                  store=BoardConfig.PLAYER_TWO_STORE)
        game = Game(players=[player_one, player_two], board=board)

    if click.confirm(f'\n\n{player_one.name.upper()} vs {player_two.name.upper()}. \n Start Game',
                     abort=True):
        game.move(player_one)


if __name__ == '__main__':
    setup()
