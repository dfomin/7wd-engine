from dataclasses import dataclass, field
from typing import Dict, Any, List

from .bonuses import BONUSES, INSTANT_BONUSES


@dataclass
class ProgressToken:
    name: str
    bonuses: Dict[int, int] = field(default_factory=dict)
    instant_bonuses: List[int] = field(default_factory=list)

    @property
    def points(self) -> int:
        return self.bonuses.get(BONUSES.index("points"), 0)

    @staticmethod
    def from_dict(description: Dict[str, Any]):
        if description["effect"] is None:
            description["effect"] = {}
        bonuses = {BONUSES.index("progress_token"): 1}
        instant_bonuses = [0] * len(INSTANT_BONUSES)
        for effect_name, effect in description["effect"].items():
            if effect_name in BONUSES:
                bonuses[BONUSES.index(effect_name)] = effect
            elif effect_name in INSTANT_BONUSES:
                instant_bonuses[INSTANT_BONUSES.index(effect_name)] = effect
            elif effect in BONUSES:
                bonuses[BONUSES.index(effect)] = 1
        return ProgressToken(description["name"],
                             bonuses,
                             instant_bonuses)
