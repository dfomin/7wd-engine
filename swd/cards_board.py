import random
from typing import List, Optional

from .board_card import BoardCard
from .cards import Card
from .entity_manager import EntityManager

CLOSED_CARD = -1
CLOSED_PURPLE_CARD = -2
NO_CARD = -3

"""
For age mask
0 - no card
1 - closed card
2 - open card
"""


"""
....0.0....
...X.X.X...
..0.0.0.0..
.X.X.X.X.X.
0.0.0.0.0.0
...........
...........
"""


def card_to_string(card_id: int):
    if card_id == NO_CARD:
        return "."
    elif card_id == CLOSED_PURPLE_CARD:
        return "#"
    elif card_id == CLOSED_CARD:
        return "X"
    else:
        return f"{card_id}"


class CardsBoard:
    card_places: List[List[BoardCard]]
    cards: List[Card]
    purple_cards: List[Card]
    preset: Optional[List[List[List[Card]]]]

    def __init__(self):
        self.card_places = []
        self.cards = []
        self.purple_cards = []
        self.preset = None

    def assign_card(self, board_card: BoardCard):
        if self.preset is not None:
            board_card.card = self.preset[board_card.age][board_card.row][board_card.column]
        elif board_card.is_purple_back:
            random.shuffle(self.purple_cards)
            board_card.card = self.purple_cards.pop()
        else:
            random.shuffle(self.cards)
            board_card.card = self.cards.pop()

    def available_cards(self) -> List[BoardCard]:
        return [card for row in self.card_places for card in row if card.is_available]

    def take_card(self, card: Card):
        board_cards = [board_card for board_card in self.available_cards() if board_card.card.id == card.id]
        if len(board_cards) != 1:
            raise ValueError
        board_card = board_cards[0]
        for child in board_card.children:
            child.remove_parent(board_card)
            if child.is_available and child.card is None:
                self.assign_card(child)
        board_card.children.clear()

        self.card_places[board_card.row][board_card.column].is_taken = True

    def generate_age(self, age: int):
        if age == 0:
            self._generate_age_1()
        elif age == 1:
            self._generate_age_2()
        elif age == 2:
            self._generate_age_3()
        else:
            raise ValueError

    def _generate_age_1(self):
        self.cards = [EntityManager.card(x) for x in range(23)]
        self.card_places = []
        for i in range(5):
            row: List[BoardCard] = []
            for j in range(i + 2):
                board_card = BoardCard(0, i, j)
                if i % 2 == 0:
                    self.assign_card(board_card)
                if i > 0:
                    if j > 0:
                        self.card_places[-1][j - 1].add_parent(board_card)
                    if j < len(self.card_places[-1]):
                        self.card_places[-1][j].add_parent(board_card)
                row.append(board_card)
            self.card_places.append(row)

    def _generate_age_2(self):
        self.cards = [EntityManager.card(x) for x in range(23, 46)]
        self.card_places = []
        for i in range(5):
            row: List[BoardCard] = []
            for j in range(6 - i):
                board_card = BoardCard(1, i, j)
                if i % 2 == 0:
                    self.assign_card(board_card)
                if i > 0:
                    self.card_places[-1][j].add_parent(board_card)
                    self.card_places[-1][j + 1].add_parent(board_card)
                row.append(board_card)
            self.card_places.append(row)

    def _generate_age_3(self):
        self.cards = [EntityManager.card(x) for x in range(46, 66)]
        self.purple_cards = [EntityManager.card(x) for x in range(66, 73)]
        self.card_places = []
        purple_indices = random.sample(range(20), k=3)
        index = 0
        for i in range(7):
            row: List[BoardCard] = []
            for j in range([2, 3, 4, 2, 4, 3, 2][i]):
                board_card = BoardCard(2, i, j)
                if index in purple_indices:
                    board_card.is_purple_back = True
                if i % 2 == 0:
                    self.assign_card(board_card)
                if i in [1, 2]:
                    if j > 0:
                        self.card_places[-1][j - 1].add_parent(board_card)
                    if j < len(self.card_places[-1]):
                        self.card_places[-1][j].add_parent(board_card)
                elif i == 3:
                    self.card_places[-1][2 * j].add_parent(board_card)
                    self.card_places[-1][2 * j + 1].add_parent(board_card)
                elif i == 4:
                    self.card_places[-1][j // 2].add_parent(board_card)
                    self.card_places[-1][j // 2].add_parent(board_card)
                elif i > 4:
                    self.card_places[-1][j].add_parent(board_card)
                    self.card_places[-1][j + 1].add_parent(board_card)
                row.append(board_card)
                index += 1
            self.card_places.append(row)

    def clone(self) -> 'CardsBoard':
        cards_board = CardsBoard()
        for row in self.card_places:
            new_row = []
            for board_card in row:
                new_card = board_card.clone()
                new_row.append(new_card)
            cards_board.card_places.append(new_row)
        for row_id in range(len(self.card_places)):
            row = self.card_places[row_id]
            new_row = cards_board.card_places[row_id]
            for column_id in range(len(row)):
                for parent in self.card_places[row_id][column_id].parents:
                    index = self.card_places[row_id + 1].index(parent)
                    new_row[column_id].add_parent(cards_board.card_places[row_id + 1][index])
        cards_board.cards = [EntityManager.card(card.id) for card in self.cards]
        cards_board.purple_cards = [EntityManager.card(card.id) for card in self.purple_cards]
        cards_board.preset = self.preset
        return cards_board
