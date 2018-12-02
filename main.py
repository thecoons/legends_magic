import sys
import math
import unittest

from io import StringIO
from unittest.mock import patch


class Action:
    action_buffer = ''

    @classmethod
    def pass_turn(cls):
        cls.action_buffer += 'PASS;'

    @classmethod
    def summon(cls, target_id):
        cls.action_buffer += 'SUMMON {};'.format(target_id)

    @classmethod
    def attack(cls, source_id, target_id):
        cls.action_buffer += 'ATTACK {} {};'.format(
            source_id,
            target_id
        )

    @classmethod
    def flush(cls):
        print(cls.action_buffer[:-1])
        cls.action_buffer = ''


class Game:
    def init_turn():
        for i in range(2):
            player_health, player_mana, player_deck, player_rune, player_draw = [
                int(j) for j in input().split()
            ]
        opponent_hand, opponent_actions = [int(i) for i in input().split()]
        for i in range(opponent_actions):
            # card_number_and_action = input()
            _ = input()
        card_count = int(input())
        for i in range(card_count):
            card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw = input().split()
            card_number = int(card_number)
            instance_id = int(instance_id)
            location = int(location)
            card_type = int(card_type)
            cost = int(cost)
            attack = int(attack)
            defense = int(defense)
            my_health_change = int(my_health_change)
            opponent_health_change = int(opponent_health_change)
            card_draw = int(card_draw)
            print("PASS")

    def run(self):
        while True:
            self.init_turn()

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)


# game loop


#########
# TESTS #
#########
class TestActionMethods(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_action_are_chained(self, mock_stdout):
        Action.summon(1)
        Action.attack(1, 2)
        Action.pass_turn()
        Action.flush()
        self.assertEqual('SUMMON 1;ATTACK 1 2;PASS\n', mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_action_buffer_is_flush(self, mock_stdout):
        Action.pass_turn()
        Action.flush()
        Action.pass_turn()
        self.assertEqual('PASS\n', mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()