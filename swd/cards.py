from dataclasses import dataclass, field
from typing import Dict, Any

import numpy as np

from .price import Price
from .bonuses import InstantBonus, BONUSES


@dataclass
class Card:
    id: int
    name: str
    price: Price
    bonuses: np.ndarray = field(default_factory=lambda: np.zeros(len(BONUSES), dtype=int))
    instant_bonus: Dict[InstantBonus, int] = field(default_factory=dict)

    @property
    def points(self) -> int:
        return self.bonuses[BONUSES.index("points")]

    @staticmethod
    def from_dict(description: Dict[str, Any]):
        if description["effect"] is None:
            description["effect"] = {}
        bonuses = np.zeros(len(BONUSES), dtype=int)
        instant_bonus = {}
        bonuses[BONUSES.index(description["color"])] += 1
        for effect_name, effect in description["effect"].items():
            if effect_name in BONUSES:
                bonuses[BONUSES.index(effect_name)] = effect
            elif effect_name in map(lambda x: x.value, InstantBonus):
                instant_bonus[InstantBonus(effect_name)] = effect
            elif effect in BONUSES:
                bonuses[BONUSES.index(effect)] = 1
            else:
                raise ValueError
        return Card(description["id"],
                    description["name"],
                    Price(description["price"]),
                    bonuses,
                    instant_bonus)
