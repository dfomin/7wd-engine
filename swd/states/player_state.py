from dataclasses import dataclass, field
from typing import List, Tuple, Optional

from ..bonuses import BONUSES


@dataclass
class PlayerState:
    index: int
    coins: int = 7
    cards: List[int] = field(default_factory=list)
    wonders: List[Tuple[int, Optional[int]]] = field(default_factory=list)
    progress_tokens: List[str] = field(default_factory=list)
    bonuses: List[int] = field(default_factory=lambda: [0] * len(BONUSES))

    def clone(self) -> 'PlayerState':
        return PlayerState(self.index,
                           self.coins,
                           self.cards.copy(),
                           self.wonders.copy(),
                           self.progress_tokens.copy(),
                           self.bonuses.copy())
