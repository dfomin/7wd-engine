from dataclasses import dataclass, field

import numpy as np


MILITARY_TOKENS_COUNT = 4


@dataclass(slots=True)
class MilitaryTrackState:
    conflict_pawn: int = 0
    military_tokens: np.ndarray = field(default_factory=lambda: np.ones(MILITARY_TOKENS_COUNT, dtype=int))

    def clone(self) -> 'MilitaryTrackState':
        return MilitaryTrackState(self.conflict_pawn,
                                  self.military_tokens.copy())
