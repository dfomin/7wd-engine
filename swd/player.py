from collections import defaultdict
from typing import Optional, List, Dict

import numpy as np

from .assets import Assets
from .bonuses import BonusManager, RESOURCES_RANGE, GENERAL_RESOURCES_RANGE, CHAIN_SYMBOLS_RANGE
from .cards import Card
from .entity_manager import EntityManager
from .progress_tokens import ProgressToken
from .wonders import Wonder


class Player:
    index: int
    coins: int
    cards: List[Card]
    wonders: List[Wonder]
    progress_tokens: List[ProgressToken]
    bonuses: Dict[int, int]

    def __init__(self, index: int):
        self.index = index
        self.coins = 7
        self.cards = []
        self.wonders = []
        self.progress_tokens = []
        self.bonuses = defaultdict(int)

    @property
    def has_masonry(self) -> bool:
        return self.has_progress_token("masonry")

    @property
    def has_architecture(self) -> bool:
        return self.has_progress_token("architecture")

    @property
    def has_urbanism(self) -> bool:
        return self.has_progress_token("urbanism")

    @property
    def has_theology(self) -> bool:
        return self.has_progress_token("theology")

    @property
    def has_economy(self) -> bool:
        return self.has_progress_token("economy")

    @property
    def has_strategy(self) -> bool:
        return self.has_progress_token("strategy")

    @property
    def scientific_symbols(self) -> List[int]:
        return BonusManager.scientific_bonuses(self.bonuses)

    @property
    def scientific_symbols_count(self) -> int:
        return BonusManager.scientific_bonuses_count(self.bonuses)

    @property
    def scientific_doubles_count(self) -> int:
        return BonusManager.scientific_doubles_count(self.bonuses)

    @property
    def blue_cards(self) -> int:
        return len([card for card in self.cards if card.is_blue])

    @property
    def brown_cards(self) -> int:
        return len([card for card in self.cards if card.is_brown])

    @property
    def gray_cards(self) -> int:
        return len([card for card in self.cards if card.is_gray])

    @property
    def yellow_cards(self) -> int:
        return len([card for card in self.cards if card.is_yellow])

    @property
    def red_cards(self) -> int:
        return len([card for card in self.cards if card.is_red])

    @property
    def green_cards(self) -> int:
        return len([card for card in self.cards if card.is_green])

    @property
    def bonus_points(self) -> int:
        return BonusManager.get_bonus("points", self.bonuses)

    @property
    def blue_points(self) -> int:
        return BonusManager.get_bonus("blue_points", self.bonuses)

    @property
    def discard_bonus(self) -> int:
        return 2 + BonusManager.get_bonus("yellow", self.bonuses)

    @property
    def built_wonders(self) -> int:
        return len([wonder for wonder in self.wonders if wonder.is_built])

    def has_progress_token(self, progress_token: str) -> bool:
        return BonusManager.has_bonus(progress_token, self.bonuses)

    def assets(self, opponent_bonuses: Dict[int, int], card: Optional[Card]) -> Assets:
        resources = np.zeros(8, dtype=int)
        resources[:5] = np.array([self.bonuses.get(x, 0) for x in RESOURCES_RANGE])
        resources[5:7] = np.array([self.bonuses.get(x, 0) for x in GENERAL_RESOURCES_RANGE])
        if card is not None:
            resources[7] = 2 if self.has_masonry and card.is_blue else 0
        else:
            resources[7] = 2 if self.has_architecture else 0
        opponents_resources = np.array([opponent_bonuses.get(x, 0) + 2 for x in range(5)])
        for i in range(7, 12):
            if self.bonuses.get(i, 0) > 0:
                opponents_resources[i - 7] = 1
        chain_symbols = np.array([self.bonuses.get(x, 0) for x in CHAIN_SYMBOLS_RANGE])
        return Assets(self.coins, resources, opponents_resources, chain_symbols, self.has_urbanism)

    def add_bonuses(self, bonuses: Dict[int, int]):
        for bonus, value in bonuses.items():
            self.bonuses[bonus] += value

    def remove_bonuses(self, bonuses: Dict[int, int]):
        for bonus, value in bonuses.items():
            if self.bonuses[bonus] == value:
                del self.bonuses[bonus]
            else:
                self.bonuses[bonus] -= value

    def add_card(self, card: Card):
        self.cards.append(card)
        self.add_bonuses(card.bonuses)

    def destroy_card(self, card: Card):
        self.cards = [x for x in self.cards if x.id != card.id]
        self.remove_bonuses(card.bonuses)

    def add_wonder(self, wonder: Wonder):
        self.wonders.append(wonder)

    def build_wonder(self, wonder: Wonder, card: Card):
        wonder.card = card
        self.add_bonuses(wonder.bonuses)

    def add_progress_token(self, progress_token: ProgressToken):
        self.progress_tokens.append(progress_token)
        self.add_bonuses(progress_token.bonuses)

    def remove_unbuilt_wonders(self):
        self.wonders = [wonder for wonder in self.wonders if wonder.is_built]

    def card_price(self, card: Card, opponent_bonuses: Dict[int, int]) -> int:
        return self.assets(opponent_bonuses, card).coins_for_price(card.price)

    def wonder_price(self, wonder: Wonder, opponent_bonuses: Dict[int, int]) -> int:
        return self.assets(opponent_bonuses, None).coins_for_price(wonder.price)

    def clone(self) -> 'Player':
        player = Player(self.index)
        player.coins = self.coins
        player.cards = [EntityManager.card(card.id) for card in self.cards]
        player.wonders = [EntityManager.wonder(wonder.id) for wonder in self.wonders]
        player.progress_tokens = [EntityManager.progress_token(token.id) for token in self.progress_tokens]
        player.bonuses = self.bonuses.copy()
        return player
