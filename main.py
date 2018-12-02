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
    def pick_card(cls, id_target):
        cls.action_buffer += 'PICK {};'.format(id_target)

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


class Player:
    def __init__(self, health, mana, deck, rune, draw):
        self.health = health
        self.mana = mana
        self.deck = deck
        self.rune = rune
        self.draw = draw

    def __repr__(self):
        return '{} {} {} {} {}'.format(
            self.health,
            self.mana,
            self.deck,
            self.rune,
            self.draw,
        )


class AllyPlayer(Player):
    pass


class EnnemyPlayer(Player):
    def __init__(self, hand_size, action_size, actions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hand_size = hand_size
        self.action_size = action_size
        self.actions = actions


class Card:
    def __init__(
        self,
        card_number,
        instance_id,
        location,
        card_type,
        cost,
        attack,
        defense,
        abilities,
        my_health_change,
        opponent_health_change,
        card_draw
    ):
        self.card_number = card_number
        self.instance_id = instance_id
        self.location = location
        self.card_type = card_type
        self.cost = cost
        self.attack = attack
        self.defense = defense
        self.abilities = abilities
        self.my_health_change = my_health_change
        self.opponent_health_change = opponent_health_change
        self.card_draw = card_draw

    def __repr__(self):
        return '{} {} {} {}'.format(
            self.card_number,
            self.instance_id,
            self.location,
            self.card_type
        )


class HiddenCard(Card):
    pass


class VisibleCard(Card):
    pass


class Board:
    def __init__(self, size, cards):
        self.size = size
        self.cards = cards


class Game:
    def __init__(self):
        self.ally_player = None
        self.ennemy_player = None
        self.board = None

    def _get_next_data_row(self):
        return [int(j) for j in input().split()]

    def _init_ally(self):
        args_ally_player = self._get_next_data_row()
        self.ally_player = AllyPlayer(*args_ally_player)

    def _init_ennemy(self):
        args_ennemy_player = self._get_next_data_row()
        args_ennemy_extra = self._get_next_data_row()
        ennemy_actions = []
        for i in range(args_ennemy_extra[-1]):
            ennemy_actions.append(input())
        args_ennemy_extra.append(ennemy_actions)
        args_ennemy_player = args_ennemy_extra + args_ennemy_player
        self.ennemy_player = EnnemyPlayer(*args_ennemy_player)

    def _init_board(self):
        args_board = [int(input())]
        board_cards = []
        for i in range(args_board[0]):
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
            board_cards.append(
                Card(
                    card_number,
                    instance_id,
                    location,
                    card_type,
                    cost,
                    attack,
                    defense,
                    abilities,
                    my_health_change,
                    opponent_health_change,
                    card_draw
                )
            )
        args_board.append(board_cards)
        self.board = Board(*args_board)

    def init_turn(self):
        self._init_ally()
        self._init_ennemy()
        self._init_board()

    def pick_up_draft(self):
        best_score = -1
        choosen_card = -1
        for index, card in enumerate(self.board.cards):
            card_score = (card.attack + card.defense)/card.cost
            if card_score > best_score:
                best_score = card_score
                choosen_card = index

        Action.pick_card(choosen_card)

    def run(self):
        while True:
            self.init_turn()
            self.pick_up_draft()
            sys.stderr.write(str(game.board.__dict__))
            Action.flush()


if __name__ == '__main__':
    game = Game()
    game.run()