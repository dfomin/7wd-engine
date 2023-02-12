from dataclasses import dataclass, field
from typing import Dict, Any, List

from .price import Price
from .bonuses import BONUSES, INSTANT_BONUSES


@dataclass
class Card:
    id: int
    name: str
    price: Price
    bonuses: Dict[int, int] = field(default_factory=dict)
    instant_bonuses: List[int] = field(default_factory=list)

    @property
    def points(self) -> int:
        return self.bonuses.get(BONUSES.index("points"), 0)

    @staticmethod
    def from_dict(description: Dict[str, Any]):
        if description["effect"] is None:
            description["effect"] = {}
        bonuses = {}
        instant_bonuses = [0] * len(INSTANT_BONUSES)
        bonuses[BONUSES.index(description["color"])] = 1
        for effect_name, effect in description["effect"].items():
            if effect_name in BONUSES:
                bonuses[BONUSES.index(effect_name)] = effect
            elif effect_name in INSTANT_BONUSES:
                instant_bonuses[INSTANT_BONUSES.index(effect_name)] = effect
            elif effect in BONUSES:
                bonuses[BONUSES.index(effect)] = 1
            else:
                raise ValueError
        return Card(description["id"],
                    description["name"],
                    Price(description["price"]),
                    bonuses,
                    instant_bonuses)
