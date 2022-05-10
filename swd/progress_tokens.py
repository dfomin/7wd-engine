from dataclasses import dataclass, field
from typing import Dict, Any

import numpy as np

from .bonuses import ImmediateBonus, BONUSES


@dataclass(slots=True)
class ProgressToken:
    name: str
    bonuses: np.ndarray = field(default_factory=lambda: np.zeros(len(BONUSES), dtype=int))
    immediate_bonus: Dict[ImmediateBonus, int] = field(default_factory=dict)

    @property
    def points(self) -> int:
        return self.bonuses[BONUSES.index("points")]

    @staticmethod
    def from_dict(description: Dict[str, Any]):
        if description["effect"] is None:
            description["effect"] = {}
        bonuses = np.zeros(len(BONUSES), dtype=int)
        bonuses[BONUSES.index("progress_token")] += 1
        if "scientific_symbol" in description:
            bonuses[BONUSES.index(description["scientific_symbol"])] += 1
        immediate_bonus = {}
        for effect_name, effect in description["effect"].items():
            if effect_name in BONUSES:
                bonuses[BONUSES.index(effect_name)] = effect
            elif effect_name in map(lambda x: x.value, ImmediateBonus):
                immediate_bonus[ImmediateBonus(effect_name)] = effect
        return ProgressToken(description["name"],
                             bonuses,
                             immediate_bonus)
