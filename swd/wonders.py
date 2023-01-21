from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List

import numpy as np

from .price import Price
from .bonuses import BONUSES, INSTANT_BONUSES


@dataclass
class Wonder:
    id: int
    name: str
    price: Price
    bonuses: Dict[int, int] = field(default_factory=dict)
    instant_bonuses: List[int] = field(default_factory=list)
    card_id: Optional[int] = None

    @property
    def is_built(self):
        return self.card_id is not None

    @property
    def points(self) -> int:
        return self.bonuses.get(BONUSES.index("points"), 0)

    @staticmethod
    def from_dict(description: Dict[str, Any]):
        if description["effect"] is None:
            description["effect"] = {}
        bonuses = {}
        instant_bonuses = [0] * len(INSTANT_BONUSES)
        for effect_name, effect in description["effect"].items():
            if effect_name in BONUSES:
                bonuses[BONUSES.index(effect_name)] = effect
            elif effect_name in INSTANT_BONUSES:
                instant_bonuses[INSTANT_BONUSES.index(effect_name)] = effect
            else:
                raise ValueError
        return Wonder(description["id"],
                      description["name"],
                      Price(description["price"]),
                      bonuses,
                      instant_bonuses,
                      None)
