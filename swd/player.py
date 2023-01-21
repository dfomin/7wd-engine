from typing import Optional, List

import numpy as np

from .assets import Assets
from .cards import Card
from .entity_manager import EntityManager
from .progress_tokens import ProgressToken
from .bonuses import BONUSES, RESOURCE_RANGE, GENERAL_RESOURCES_RANGE, TRADE_RESOURCES_RANGE, SCIENTIFIC_SYMBOLS_RANGE,\
    CHAIN_SYMBOLS_RANGE
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
    def assets(state: PlayerState, opponents_resources: List[int], card: Optional[Card]) -> Assets:
        resources = list(Player.resources(state)) + list(Player.general_resources(state)) + [0]
        if card is not None:
            if card.bonuses[BONUSES.index("blue")] > 0:
                resources[7] = 2 if state.bonuses[BONUSES.index("masonry")] > 0 else 0
        else:
            resources[7] = 2 if state.bonuses[BONUSES.index("architecture")] > 0 else 0
        opponents_resources = [1 if t else r + 2 for r, t in zip(opponents_resources, Player.trade_resources(state))]
        urbanism = state.bonuses[BONUSES.index("urbanism")] > 0
        return Assets(state.coins, resources, opponents_resources, list(Player.chain_symbols(state)), urbanism)

    @staticmethod
    def resources(state: PlayerState) -> List[int]:
        return state.bonuses[RESOURCE_RANGE]

    @staticmethod
    def general_resources(state: PlayerState) -> List[int]:
        return state.bonuses[GENERAL_RESOURCES_RANGE]

    @staticmethod
    def trade_resources(state: PlayerState) -> List[int]:
        return state.bonuses[TRADE_RESOURCES_RANGE]

    @staticmethod
    def scientific_symbols(state: PlayerState) -> List[int]:
        return state.bonuses[SCIENTIFIC_SYMBOLS_RANGE]

    @staticmethod
    def chain_symbols(state: PlayerState) -> List[int]:
        return state.bonuses[CHAIN_SYMBOLS_RANGE]

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
        return Player.assets(state, Player.resources(opponent_state), card).coins_for_price(card.price)

    @staticmethod
    def wonder_price(state: PlayerState, wonder: Wonder, opponent_state: PlayerState) -> int:
        return Player.assets(state, Player.resources(opponent_state), None).coins_for_price(wonder.price)
