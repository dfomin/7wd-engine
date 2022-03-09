from dataclasses import dataclass, field
from typing import Dict, Any, Optional

import numpy as np

from .price import Price
from .bonuses import CoinsAndResources, ImmediateBonus, RESOURCES, BONUSES


@dataclass
class Wonder:
    id: int
    name: str
    price: Price
    bonuses: np.ndarray = field(default_factory=lambda: np.zeros(len(BONUSES), dtype=int))
    immediate_bonus: Dict[ImmediateBonus, int] = field(default_factory=dict)
    card_id: Optional[int] = None

    @property
    def is_built(self):
        return self.card_id is not None

    @property
    def points(self) -> int:
        return self.bonuses[BONUSES.index("points")]

    @staticmethod
    def from_dict(description: Dict[str, Any]):
        if description["effect"] is None:
            description["effect"] = {}
        price = CoinsAndResources({k: (description["price"] or {}).get(k, 0) for k in RESOURCES + ["coins"]})
        bonuses = np.zeros(len(BONUSES), dtype=int)
        immediate_bonus = {}
        for effect_name, effect in description["effect"].items():
            if effect_name in BONUSES:
                bonuses[BONUSES.index(effect_name)] = effect
            elif effect_name in map(lambda x: x.value, ImmediateBonus):
                immediate_bonus[ImmediateBonus(effect_name)] = effect
            else:
                raise ValueError
        return Wonder(description["id"],
                      description["name"],
                      Price(price.coins, price.resources, -1),
                      bonuses,
                      immediate_bonus,
                      None)
