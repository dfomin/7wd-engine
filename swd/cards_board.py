import random
from typing import List, Optional

from .board_card import BoardCard
from .cards import Card

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
    preset: Optional[List[List[List[BoardCard]]]]

    def __init__(self):
        self.card_places = []
        self.cards = []
        self.purple_cards = []
        self.preset = None

    def get_card(self, board_card: BoardCard, age: int):
        if self.preset is not None:
            return self.preset[age][board_card.row][board_card.column]
        elif board_card.is_purple_back:
            random.shuffle(self.purple_cards)
            board_card.card = self.purple_cards.pop()
        else:
            random.shuffle(self.cards)
            board_card.card = self.cards.pop()

    def available_cards(self) -> List[BoardCard]:
        return [card for row in self.card_places for card in row if card.is_available]

    def take_card(self, board_card: BoardCard):
        for child in board_card.children:
            child.remove_parent(board_card)
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
        self.cards = list(range(23))
        for i in range(5):
            row: List[BoardCard] = []
            for j in range(i + 2):
                board_card = BoardCard(i, j)
                if i % 2 == 0:
                    board_card.card = self.get_card(board_card, 0)
                if i > 0:
                    if j > 0:
                        self.card_places[-1][j - 1].add_parent(board_card)
                    if j < len(self.card_places[-1]):
                        self.card_places[-1][j].add_parent(board_card)
                row.append(board_card)
            self.card_places.append(row)

    def _generate_age_2(self):
        self.cards = list(range(23, 46))
        for i in range(5):
            row: List[BoardCard] = []
            for j in range(6 - i):
                board_card = BoardCard(i, j)
                if i % 2 == 0:
                    board_card.card = self.get_card(board_card, 1)
                if i > 0:
                    self.card_places[-1][j].add_parent(board_card)
                    self.card_places[-1][j + 1].add_parent(board_card)
                row.append(board_card)
            self.card_places.append(row)

    def _generate_age_3(self):
        self.cards = list(range(46, 66))
        self.purple_cards = list(range(66, 73))
        purple_indices = random.sample(range(20), k=3)
        index = 0
        for i in range(7):
            row: List[BoardCard] = []
            for j in range([2, 3, 4, 2, 4, 3, 2][i]):
                board_card = BoardCard(i, j)
                if index in purple_indices:
                    board_card.is_purple_back = True
                if i % 2 == 0:
                    board_card.card = self.get_card(board_card, 2)
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
