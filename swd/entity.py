from typing import Dict, Any

from swd.bonuses import BonusManager, BONUSES_INDEX, INSTANT_BONUSES_INDEX


class Entity:
    id: int
    name: str
    bonuses: Dict[int, int]
    instant_bonuses: Dict[int, int]

    def __init__(self, description: Dict[str, Any]):
        if description["effect"] is None:
            description["effect"] = {}
        bonuses, instant_bonuses = BonusManager.from_dict(description["effect"])

        self.id = description["id"]
        self.name = description["name"]
        self.bonuses = bonuses
        self.instant_bonuses = instant_bonuses

    def has_bonus(self, bonus: str) -> bool:
        return self.get_bonus(bonus) > 0

    def get_bonus(self, bonus: str) -> int:
        if bonus in BONUSES_INDEX:
            return BonusManager.get_bonus(bonus, self.bonuses)
        elif bonus in INSTANT_BONUSES_INDEX:
            return BonusManager.get_instant_bonus(bonus, self.instant_bonuses)
        else:
            raise ValueError

    @property
    def points(self) -> int:
        return self.get_bonus("points")
