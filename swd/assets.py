from dataclasses import dataclass

import numpy as np

from .price import Price


@dataclass(slots=True)
class Assets:
    coins: int
    resources: np.ndarray
    resources_cost: np.ndarray
    chain_symbols: np.ndarray
    urbanism: bool

    def coins_for_price(self, price: Price) -> int:
        if price.chain_symbol >= 0 and self.chain_symbols[price.chain_symbol]:
            return -4 if self.urbanism else 0

        price_resources = price.resources.copy()

        assets = np.zeros((3, 5), dtype=int)
        assets[0] = np.arange(5)
        assets[1][:3] = 5
        assets[1][3:] = 6
        assets[2] = 7

        most_expensive_indices = (-self.resources_cost).argsort()
        for index in most_expensive_indices:
            for i in range(3):
                amount = min(price_resources[index], self.resources[assets[i, index]])
                price_resources[index] -= amount
                self.resources[assets[i, index]] -= amount
                if price_resources[index] == 0:
                    break
        cost = np.sum(price_resources * self.resources_cost)
        return price.coins + cost
