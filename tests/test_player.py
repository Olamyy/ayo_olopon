import unittest
from ayo.player import Player
from ayo.settings import BoardConfig


class PlayerTest(unittest.TestCase):
    """
    Player Tests
    """

    def setUp(self):
        self.player_one = Player(name="Olamilekan Wahab",
                                 pits=4,
                                 store=0)
        self.player_two = Player(name="Mufrad Wahab",
                                 pits=4,
                                 store=3)

    def test_player_name_is_valid(self):
        self.assertEqual(self.player_one.name, "Olamilekan Wahab")

    def test_check_pits_is_valid_for_player(self):
        pass
