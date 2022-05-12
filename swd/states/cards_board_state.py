from dataclasses import dataclass
from typing import Optional

import numpy as np


@dataclass
class CardsBoardState:
    age: int
    card_places: np.ndarray
    card_ids: np.ndarray
    purple_card_ids: np.ndarray
    preset: Optional[np.ndarray]

    def clone(self) -> 'CardsBoardState':
        return CardsBoardState(self.age,
                               self.card_places.copy(),
                               self.card_ids.copy(),
                               self.purple_card_ids.copy(),
                               self.preset.copy() if self.preset is not None else None)
