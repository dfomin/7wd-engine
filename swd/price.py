from dataclasses import dataclass
from typing import Dict

import numpy as np

from swd.bonuses import RESOURCES, CHAIN_SYMBOLS


@dataclass
class Price:
    coins: int
    resources: np.ndarray
    chain_symbol: int = -1

    def __init__(self, description: Dict[str, int] = None):
        if description is None:
            description = {}
        self.coins = description.get("coins", 0)
        self.resources = np.zeros(len(RESOURCES), dtype=int)
        for i, effect_name in enumerate(RESOURCES):
            self.resources[i] = description.get(effect_name, 0)
        for effect in description.values():
            if effect in CHAIN_SYMBOLS:
                self.chain_symbol = CHAIN_SYMBOLS.index(effect)
                break
