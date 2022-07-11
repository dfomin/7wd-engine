from dataclasses import dataclass, field
from typing import Dict, Any, Optional

import numpy as np

from .price import Price
from .bonuses import InstantBonus, BONUSES


@dataclass
class Wonder:
    id: int
    name: str
    price: Price
    bonuses: np.ndarray = field(default_factory=lambda: np.zeros(len(BONUSES), dtype=int))
    instant_bonus: Dict[InstantBonus, int] = field(default_factory=dict)
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
        bonuses = np.zeros(len(BONUSES), dtype=int)
        instant_bonus = {}
        for effect_name, effect in description["effect"].items():
            if effect_name in BONUSES:
                bonuses[BONUSES.index(effect_name)] = effect
            elif effect_name in map(lambda x: x.value, InstantBonus):
                instant_bonus[InstantBonus(effect_name)] = effect
            else:
                raise ValueError
        return Wonder(description["id"],
                      description["name"],
                      Price(description["price"]),
                      bonuses,
                      instant_bonus,
                      None)
