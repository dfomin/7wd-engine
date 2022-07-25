from typing import Optional, List, Dict

import numpy as np

from .assets import Assets
from .cards import Card
from .entity_manager import EntityManager
from .progress_tokens import ProgressToken
from .states.player_state import PlayerState
from .wonders import Wonder


class Player:
    @staticmethod
    def wonders(state: PlayerState) -> List[Wonder]:
        result = []
        for wonder_id, card_id in state.wonders:
            wonder = EntityManager.wonder(wonder_id)
            wonder.card_id = card_id
            result.append(wonder)
        return result

    @staticmethod
    def cards(state: PlayerState) -> List[Card]:
        return [EntityManager.card(card_id) for card_id in state.cards]

    @staticmethod
    def progress_tokens(state: PlayerState) -> List[ProgressToken]:
        return [EntityManager.progress_token(token_name) for token_name in state.progress_tokens]

    @staticmethod
    def assets(state: PlayerState, opponent_bonuses: Dict[int, int], card: Optional[Card]) -> Assets:
        resources = np.zeros(8, dtype=int)
        resources[:5] = np.array([state.bonuses.get(x, 0) for x in range(5)])
        resources[5:7] = np.array([state.bonuses.get(x, 0) for x in range(5, 7)])
        if card is not None:
            resources[7] = 2 if state.has_masonry and card.is_blue else 0
        else:
            resources[7] = 2 if state.has_architecture else 0
        opponents_resources = np.array([opponent_bonuses.get(x, 0) + 2 for x in range(5)])
        for i in range(7, 12):
            if state.bonuses.get(i, 0) > 0:
                opponents_resources[i - 7] = 1
        chain_symbols = np.ndarray([state.bonuses.get(x, 0) for x in range(12, 12 + 17)])
        return Assets(state.coins, resources, opponents_resources, chain_symbols, state.has_urbanism)

    @staticmethod
    def add_card(state: PlayerState, card: Card):
        state.cards.append(card.id)
        state.bonuses += card.bonuses

    @staticmethod
    def destroy_card(state: PlayerState, card_id: int):
        state.cards.remove(card_id)
        state.bonuses -= EntityManager.card(card_id).bonuses

    @staticmethod
    def add_wonder(state: PlayerState, wonder_id: int):
        state.wonders.append((wonder_id, None))

    @staticmethod
    def build_wonder(state: PlayerState, wonder_id: int, card_id: int):
        for i, wonder in enumerate(state.wonders):
            if wonder[0] == wonder_id:
                if wonder[1] is not None:
                    raise ValueError
                state.wonders[i] = wonder_id, card_id
                state.bonuses += EntityManager.wonder(wonder_id).bonuses
                return
        raise ValueError

    @staticmethod
    def add_progress_token(state: PlayerState, progress_token: ProgressToken):
        state.progress_tokens.append(progress_token.name)
        state.bonuses += progress_token.bonuses

    @staticmethod
    def remove_unbuilt_wonders(state: PlayerState):
        state.wonders = [x for x in state.wonders if x[1] is not None]

    @staticmethod
    def card_price(state: PlayerState, card: Card, opponent_state: PlayerState) -> int:
        return Player.assets(state, opponent_state.bonuses, card).coins_for_price(card.price)

    @staticmethod
    def wonder_price(state: PlayerState, wonder: Wonder, opponent_state: PlayerState) -> int:
        return Player.assets(state, opponent_state.bonuses, None).coins_for_price(wonder.price)
