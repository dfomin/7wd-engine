from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict

from ..bonuses import BonusManager


@dataclass
class PlayerState:
    index: int
    coins: int = 7
    cards: List[int] = field(default_factory=list)
    wonders: List[Tuple[int, Optional[int]]] = field(default_factory=list)
    progress_tokens: List[int] = field(default_factory=list)
    bonuses: Dict[int, int] = field(default_factory=dict)

    @property
    def has_masonry(self) -> bool:
        return BonusManager.has_bonus("masonry", self.bonuses)

    @property
    def has_architecture(self) -> bool:
        return BonusManager.has_bonus("architecture", self.bonuses)

    @property
    def has_urbanism(self) -> bool:
        return BonusManager.has_bonus("urbanism", self.bonuses)

    def clone(self) -> 'PlayerState':
        return PlayerState(self.index,
                           self.coins,
                           self.cards.copy(),
                           self.wonders.copy(),
                           self.progress_tokens.copy(),
                           self.bonuses.copy())
