from typing import List, Tuple

import numpy as np

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

AGES = np.array([
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
    ]], dtype=int)


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
            state.card_places[pos] = state.preset[state.age, pos[0], pos[1]]
        elif state.card_places[pos] == CLOSED_CARD:
            np.random.shuffle(state.card_ids)
            state.card_places[pos] = state.card_ids[0]
            state.card_ids = state.card_ids[1:]
        elif state.card_places[pos] == CLOSED_PURPLE_CARD:
            np.random.shuffle(state.purple_card_ids)
            state.card_places[pos] = state.purple_card_ids[0]
            state.purple_card_ids = state.purple_card_ids[1:]


class CardsBoard:
    state: CardsBoardState

    @staticmethod
    def print(state: CardsBoardState):
        result = ""
        mask = AGES[state.age]
        for row in range(len(state.card_places)):
            if (mask[row] > 0).sum() == 0:
                continue
            cards = state.card_places[row][mask[row] > 0]
            result += " ".join(map(lambda x: card_to_string(x), cards)) + "\n"
        return result

    @staticmethod
    def generate_age(state: CardsBoardState):
        state._available_cards = None

        mask = AGES[state.age]
        card_places = mask + NO_CARD
        card_places[mask > 0] = CLOSED_CARD

        if state.age == 0:
            card_ids = np.arange(23)
            purple_card_ids = np.array([], dtype=int)
        elif state.age == 1:
            card_ids = np.arange(23, 46)
            purple_card_ids = np.array([], dtype=int)
        elif state.age == 2:
            card_ids = np.arange(46, 66)
            purple_card_ids = np.arange(66, 73)
            indices = np.transpose(np.where(mask > 0))
            purple_indices = np.random.choice(np.arange(len(indices)), 3, replace=False)
            for index in purple_indices:
                pos = tuple(indices[index])
                card_places[pos] = CLOSED_PURPLE_CARD
        else:
            raise ValueError

        state.card_places = card_places
        state.card_ids = card_ids
        state.purple_card_ids = purple_card_ids

        for pos in np.transpose(np.where(mask == 2)):
            OpeningCardsProvider.get_card(tuple(pos), state)

        if state.preset is not None:
            for pos in np.transpose(np.where(mask == 1)):
                pos = tuple(pos)
                if state.card_places[pos] == CLOSED_CARD and state.preset[state.age, pos[0], pos[1]] >= 66:
                    state.card_places[pos] = CLOSED_PURPLE_CARD

    @staticmethod
    def available_cards(state: CardsBoardState) -> List[Tuple[int, Tuple[int, int]]]:
        if state._available_cards is not None:
            return state._available_cards
        result = []
        places = np.where(state.card_places >= 0)
        for pos in zip(places[0], places[1]):
            is_last_row = pos[0] == state.card_places.shape[0] - 1
            is_last_column = pos[1] == state.card_places.shape[1] - 1
            if is_last_row:
                result.append((state.card_places[tuple(pos)], tuple(pos)))
            elif state.card_places[pos[0] + 1, pos[1]] == NO_CARD:
                if is_last_column or state.card_places[pos[0] + 1, pos[1] + 1] == NO_CARD:
                    result.append((state.card_places[tuple(pos)], tuple(pos)))
        state._available_cards = result
        return result

    @staticmethod
    def take_card(state: CardsBoardState, card_id: int):
        state._available_cards = None
        index = np.where(state.card_places == card_id)
        if len(index[0]) != 1 or len(index[1]) != 1:
            raise ValueError
        pos = index[0][0], index[1][0]
        state.card_places[pos] = NO_CARD
        if pos[0] > 0:
            card_up_pos = pos[0] - 1, pos[1]
            card_up_left_pos = pos[0] - 1, pos[1] - 1
            card_right_pos = pos[0], pos[1] + 1
            card_left_pos = pos[0], pos[1] - 1
            if CardsBoard.check_pos(state, card_up_pos):
                if CardsBoard.check_pos(state, card_right_pos):
                    if state.card_places[card_right_pos] == NO_CARD:
                        OpeningCardsProvider.get_card(card_up_pos, state)
                else:
                    OpeningCardsProvider.get_card(card_up_pos, state)
            if CardsBoard.check_pos(state, card_up_left_pos) and CardsBoard.check_pos(state, card_left_pos):
                if state.card_places[card_left_pos] == NO_CARD:
                    OpeningCardsProvider.get_card(card_up_left_pos, state)

    @staticmethod
    def check_pos(state: CardsBoardState, pos: Tuple[int, int]):
        return 0 <= pos[0] < state.card_places.shape[0] and 0 <= pos[1] < state.card_places.shape[1]
