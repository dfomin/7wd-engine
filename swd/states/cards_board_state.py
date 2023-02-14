from copy import deepcopy
from dataclasses import dataclass
from typing import Optional, List, Tuple


@dataclass
class CardsBoardState:
    age: int
    card_places: List[List[int]]
    card_ids: List[int]
    purple_card_ids: List[int]
    preset: Optional[List[List[List[int]]]]
    available_cards: Optional[List[Tuple[int, Tuple[int, int]]]] = None

    def clone(self) -> 'CardsBoardState':
        return CardsBoardState(self.age,
                               deepcopy(self.card_places),
                               self.card_ids.copy(),
                               self.purple_card_ids.copy(),
                               deepcopy(self.preset) if self.preset is not None else None,
                               None)
