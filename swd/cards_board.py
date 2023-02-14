import random
from typing import List, Tuple

from .states.cards_board_state import CardsBoardState

CLOSED_CARD = -1
CLOSED_PURPLE_CARD = -2
NO_CARD = -3

"""
For age mask
0 - no card
1 - closed card
2 - open card
"""

AGES = [
    [
        [2, 2, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0],
        [2, 2, 2, 2, 0, 0],
        [1, 1, 1, 1, 1, 0],
        [2, 2, 2, 2, 2, 2],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ],
    [
        [2, 2, 2, 2, 2, 2],
        [0, 1, 1, 1, 1, 1],
        [0, 0, 2, 2, 2, 2],
        [0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 2, 2],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ],
    [
        [2, 2, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0],
        [2, 2, 2, 2, 0, 0],
        [0, 1, 0, 1, 0, 0],
        [0, 2, 2, 2, 2, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 2, 2, 0],
    ]
]


def card_to_string(card_id: int):
    if card_id == NO_CARD:
        return "."
    elif card_id == CLOSED_PURPLE_CARD:
        return "#"
    elif card_id == CLOSED_CARD:
        return "X"
    else:
        return f"{card_id}"


class OpeningCardsProvider:
    @staticmethod
    def get_card(pos: Tuple[int, int], state: CardsBoardState):
        if state.preset is not None:
            state.card_places[pos[0]][pos[1]] = state.preset[state.age][pos[0]][pos[1]]
        elif state.card_places[pos[0]][pos[1]] == CLOSED_CARD:
            random.shuffle(state.card_ids)
            state.card_places[pos[0]][pos[1]] = state.card_ids.pop(0)
        elif state.card_places[pos[0]][pos[1]] == CLOSED_PURPLE_CARD:
            random.shuffle(state.purple_card_ids)
            state.card_places[pos[0]][pos[1]] = state.purple_card_ids.pop(0)


class CardsBoard:
    state: CardsBoardState

    @staticmethod
    def print(state: CardsBoardState):
        result = ""
        mask = AGES[state.age]
        for row in range(len(state.card_places)):
            if sum(mask[row]) == 0:
                continue
            cards = [x for i, x in enumerate(state.card_places[row]) if mask[row][i] > 0]
            result += " ".join(map(lambda x: card_to_string(x), cards)) + "\n"
        return result

    @staticmethod
    def generate_age(state: CardsBoardState):
        state.available_cards = None

        mask = AGES[state.age]
        card_places = [[NO_CARD if mask[i][j] == 0 else CLOSED_CARD
                        for j in range(len(mask[0]))]
                       for i in range(len(mask))]

        if state.age == 0:
            card_ids = list(range(23))
            purple_card_ids = []
        elif state.age == 1:
            card_ids = list(range(23, 46))
            purple_card_ids = []
        elif state.age == 2:
            card_ids = list(range(46, 66))
            purple_card_ids = list(range(66, 73))
            indices = [(i, j)
                       for i in range(len(mask))
                       for j in range(len(mask[0]))
                       if mask[i][j] > 0]
            purple_indices = random.sample(range(len(indices)), 3)
            for index in purple_indices:
                pos = tuple(indices[index])
                card_places[pos[0]][pos[1]] = CLOSED_PURPLE_CARD
        else:
            raise ValueError

        state.card_places = card_places
        state.card_ids = card_ids
        state.purple_card_ids = purple_card_ids

        places = [(i, j)
                  for i in range(len(mask))
                  for j in range(len(mask[0]))
                  if mask[i][j] == 2]

        for pos in places:
            OpeningCardsProvider.get_card(pos, state)

        if state.preset is not None:
            places = [(i, j)
                      for i in range(len(mask))
                      for j in range(len(mask[0]))
                      if mask[i][j] == 1]

            for pos in places:
                if state.card_places[pos[0]][pos[1]] == CLOSED_CARD and state.preset[state.age][pos[0]][pos[1]] >= 66:
                    state.card_places[pos[0]][pos[1]] = CLOSED_PURPLE_CARD

    @staticmethod
    def available_cards(state: CardsBoardState) -> List[Tuple[int, Tuple[int, int]]]:
        if state.available_cards is not None:
            return state.available_cards
        result = []
        places = [(i, j)
                  for i in range(len(state.card_places))
                  for j in range(len(state.card_places[0]))
                  if state.card_places[i][j] >= 0]
        for pos in places:
            is_last_row = pos[0] == len(state.card_places) - 1
            is_last_column = pos[1] == len(state.card_places[0]) - 1
            if is_last_row:
                result.append((state.card_places[pos[0]][pos[1]], tuple(pos)))
            elif state.card_places[pos[0] + 1][pos[1]] == NO_CARD:
                if is_last_column or state.card_places[pos[0] + 1][pos[1] + 1] == NO_CARD:
                    result.append((state.card_places[pos[0]][pos[1]], tuple(pos)))
        state.available_cards = result
        return result

    @staticmethod
    def take_card(state: CardsBoardState, card_id: int):
        pos = None
        state.available_cards = None
        for i in range(len(state.card_places)):
            for j in range(len(state.card_places[0])):
                if state.card_places[i][j] == card_id:
                    pos = i, j
        if len(pos) != 2:
            print(card_id, pos)
            print(state.card_places)
            raise ValueError
        state.card_places[pos[0]][pos[1]] = NO_CARD
        if pos[0] > 0:
            card_up_pos = pos[0] - 1, pos[1]
            card_up_left_pos = pos[0] - 1, pos[1] - 1
            card_right_pos = pos[0], pos[1] + 1
            card_left_pos = pos[0], pos[1] - 1
            if CardsBoard.check_pos(state, card_up_pos):
                if CardsBoard.check_pos(state, card_right_pos):
                    if state.card_places[card_right_pos[0]][card_right_pos[1]] == NO_CARD:
                        OpeningCardsProvider.get_card(card_up_pos, state)
                else:
                    OpeningCardsProvider.get_card(card_up_pos, state)
            if CardsBoard.check_pos(state, card_up_left_pos) and CardsBoard.check_pos(state, card_left_pos):
                if state.card_places[card_left_pos[0]][card_left_pos[1]] == NO_CARD:
                    OpeningCardsProvider.get_card(card_up_left_pos, state)

    @staticmethod
    def check_pos(state: CardsBoardState, pos: Tuple[int, int]):
        return 0 <= pos[0] < len(state.card_places) and 0 <= pos[1] < len(state.card_places[0])
