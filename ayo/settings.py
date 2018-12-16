class BaseConfig(object):
    COMPUTER_NAME = 'Iku baba yeye'
    INTRO_WAIT_TIME = 3
    GAME_TYPE_MAP = {"hvh": "Human vs Human", "hvc": "Computer vs Human", "cvc": "Computer vs Computer"}


class BoardConfig(BaseConfig):
    PLAYER_ONE_PITS = 0
    PLAYER_ONE_STORE = 1
    PLAYER_TWO_PITS = 2
    PLAYER_TWO_STORE = 3
    MAX_PITS = 6
    MAX_STONES = 4


class MessageConfig(BaseConfig):
    GAME_TYPE = """    How will you like to play ? 
                       \n1 : Human vs Human  
                        \n2 : Human vs Computer  
                        \n3 : Computer vs Computer \n"""
    PENALIZE_INVALID_MOVE = "Remove 1 point from user's point for invalid move."
    DEFAULT_PITS = "Default number of pits"
    DEFAULT_STONES = "Default number of stones"


class PlayerConfig(BaseConfig):
    # Player types
    HUMAN_PLAYER = 0
    AI_PLAYER = 1
    DEFAULT_TYPE = HUMAN_PLAYER

    # AI Profiles
    RANDOM_AI = 0  # purely random
    VECTOR_AI = 1  # optimizes for free turns only considering own side
    DEFAULT_AI = 1
