from dataclasses import dataclass
from typing import List

import numpy as np

from .price import Price


@dataclass
class Assets:
    coins: int
    resources: np.ndarray
    resources_cost: np.ndarray
    chain_symbols: np.ndarray
    urbanism: bool

    def coins_for_price(self, price: Price) -> int:
        if price.chain_symbol >= 0 and self.chain_symbols[price.chain_symbol]:
            return -4 if self.urbanism else 0

        if self.resources[5] == 0 and self.resources[6] == 0 and self.resources[7] == 0:
            cost = sum([max(p - r, 0) * c for p, r, c in zip(price.resources, self.resources, self.resources_cost)])
        else:
            needed_resources = [max(p - r, 0) for p, r in zip(price.resources, self.resources)]

            materials = [self.resources_cost[i] for i in range(3) for _ in range(needed_resources[i])]
            materials.sort(reverse=True)

            goods = [self.resources_cost[i] for i in range(3, 5) for _ in range(needed_resources[i])]
            goods.sort(reverse=True)

            rest = materials[self.resources[5]:] + goods[self.resources[6]:]
            rest.sort(reverse=True)

            cost = sum(rest[self.resources[7]:])

        return price.coins + cost
