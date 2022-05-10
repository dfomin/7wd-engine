from dataclasses import dataclass, field
from typing import Dict, Any

import numpy as np

from .price import Price
from .bonuses import CoinsAndResources, ImmediateBonus, RESOURCES, CHAIN_SYMBOLS, BONUSES


@dataclass(slots=True)
class Card:
    id: int
    name: str
    price: Price
    bonuses: np.ndarray = field(default_factory=lambda: np.zeros(len(BONUSES), dtype=int))
    immediate_bonus: Dict[ImmediateBonus, int] = field(default_factory=dict)

    @property
    def points(self) -> int:
        return self.bonuses[BONUSES.index("points")]

    @staticmethod
    def from_dict(description: Dict[str, Any]):
        if description["effect"] is None:
            description["effect"] = {}
        price = CoinsAndResources({k: (description["price"] or {}).get(k, 0) for k in RESOURCES + ["coins"]})
        chain_in = CHAIN_SYMBOLS.index(description["chain_in"]) if "chain_in" in description else -1
        bonuses = np.zeros(len(BONUSES), dtype=int)
        immediate_bonus = {}
        bonuses[BONUSES.index(description["color"])] += 1
        if "chain_out" in description:
            bonuses[BONUSES.index(description["chain_out"])] += 1
        if "scientific_symbol" in description:
            bonuses[BONUSES.index(description["scientific_symbol"])] += 1
        for effect_name, effect in description["effect"].items():
            if effect_name in BONUSES:
                bonuses[BONUSES.index(effect_name)] = effect
            elif effect_name in map(lambda x: x.value, ImmediateBonus):
                immediate_bonus[ImmediateBonus(effect_name)] = effect
            else:
                raise ValueError
        return Card(description["id"],
                    description["name"],
                    Price(price.coins, price.resources, chain_in),
                    bonuses,
                    immediate_bonus)
