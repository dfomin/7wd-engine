from collections import defaultdict
from typing import Optional, List, Dict, Tuple

import numpy as np

from .assets import Assets
from .bonuses import BonusManager
from .cards import Card
from .entity import Entity
from .entity_manager import EntityManager
from .progress_tokens import ProgressToken
from .states.player_state import PlayerState
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
        return BonusManager.has_bonus("masonry", self.bonuses)

    @property
    def has_architecture(self) -> bool:
        return BonusManager.has_bonus("architecture", self.bonuses)

    @property
    def has_urbanism(self) -> bool:
        return BonusManager.has_bonus("urbanism", self.bonuses)

    def assets(self, opponent_bonuses: Dict[int, int], card: Optional[Card]) -> Assets:
        resources = np.zeros(8, dtype=int)
        resources[:5] = np.array([self.bonuses.get(x, 0) for x in range(5)])
        resources[5:7] = np.array([self.bonuses.get(x, 0) for x in range(5, 7)])
        if card is not None:
            resources[7] = 2 if self.has_masonry and card.is_blue else 0
        else:
            resources[7] = 2 if self.has_architecture else 0
        opponents_resources = np.array([opponent_bonuses.get(x, 0) + 2 for x in range(5)])
        for i in range(7, 12):
            if self.bonuses.get(i, 0) > 0:
                opponents_resources[i - 7] = 1
        chain_symbols = np.ndarray([self.bonuses.get(x, 0) for x in range(12, 12 + 17)])
        return Assets(self.coins, resources, opponents_resources, chain_symbols, self.has_urbanism)

    def add_bonuses(self, bonuses: Dict[int, int]):
        for bonus, value in bonuses.items():
            if bonus in self.bonuses:
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
        self.cards.remove(card)
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
