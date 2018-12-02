import unittest

from io import StringIO
from unittest.mock import patch

from main import (
    Action,
    AllyPlayer,
    Board,
    Card,
    EnnemyPlayer,
    Game,
)


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
        Action.summon(1)
        Action.pass_turn()
        Action.flush()

        mock_stdout.truncate(0)
        mock_stdout.seek(0)

        Action.pass_turn()
        Action.flush()

        self.assertEqual('PASS\n', mock_stdout.getvalue())


class TestGameMethods(unittest.TestCase):
    @patch('builtins.input')
    def test_init_turn(self, input_mock):
        input_mock.side_effect = [
            # Player data
            '30 0 0 25 0',
            '30 0 0 25 0',
            # Ennemy hand size and actions size
            '0 1',
            # Actions
            '9 ATTACK 8 -1',
            # Board size
            '2',
            # Cards data
            '18 -1 0 0 4 7 4 ------ 0 0 0',
            '9 13 0 0 3 3 4 ------ 0 0 0',
        ]

        game = Game()
        game.init_turn()

        expected_ally_player = AllyPlayer(
            health=30,
            mana=0,
            deck=0,
            rune=25,
            draw=0
        )

        expected_ennemy_player = EnnemyPlayer(
            health=30,
            mana=0,
            deck=0,
            rune=25,
            draw=0,
            hand_size=0,
            action_size=1,
            actions=['9 ATTACK 8 -1']
        )

        expected_card_1 = Card(
            *[18, -1, 0, 0, 4, 7, 4, '------', 0, 0, 0]
        )
        expected_card_2 = Card(
            *[9, 13, 0, 0, 3, 3, 4, '------', 0, 0, 0]
        )

        expected_board = Board(
            size=2,
            cards=[
                expected_card_1,
                expected_card_2
            ]
        )

        self.assertIsInstance(
            game.ally_player,
            AllyPlayer
        )
        self.assertIsInstance(
            game.ennemy_player,
            EnnemyPlayer
        )
        self.assertIsInstance(
            game.board,
            Board
        )

        self.assertDictEqual(
            expected_ally_player.__dict__,
            game.ally_player.__dict__
        )

        self.assertDictEqual(
            expected_ennemy_player.__dict__,
            game.ennemy_player.__dict__
        )

        self.assertEqual(expected_board.size, game.board.size)
        self.assertEqual(
            expected_card_1.__dict__,
            game.board.cards[0].__dict__
        )
        self.assertEqual(
            expected_card_2.__dict__,
            game.board.cards[1].__dict__
        )

    @patch('builtins.input')
    def test_init_without_actions(self, input_mock):
        input_mock.side_effect = [
            # Player data
            '30 0 0 25 0',
            '30 0 0 25 0',
            # Ennemy hand size and actions size
            '0 0',
            # Board size
            '2',
            # Cards data
            '18 -1 0 0 4 7 4 ------ 0 0 0',
            '9 13 0 0 3 3 4 ------ 0 0 0',
        ]

        game = Game()
        game.init_turn()

        expected_ennemy_player = EnnemyPlayer(
            health=30,
            mana=0,
            deck=0,
            rune=25,
            draw=0,
            hand_size=0,
            action_size=0,
            actions=[]
        )

        self.assertDictEqual(
            expected_ennemy_player.__dict__,
            game.ennemy_player.__dict__
        )

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_pick_up_draft(self, stdout_mock, input_mock):
        input_mock.side_effect = [
            # Player data
            '30 0 0 25 0',
            '30 0 0 25 0',
            # Ennemy hand size and actions size
            '0 0',
            # Board size
            '3',
            # Cards data
            '18 -1 0 0 99 0 0 ------ 0 0 0',
            '9 -1 0 0 1 99 99 ------ 0 0 0',
            '7 -1 0 0 99 0 0 ------ 0 0 0',
        ]

        game = Game()
        game.init_turn()
        game.pick_up_draft()
        Action.flush()

        self.assertEqual('PICK 1\n', stdout_mock.getvalue())

if __name__ == '__main__':
    unittest.main()
