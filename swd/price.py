from dataclasses import dataclass

import numpy as np


@dataclass
class Price:
    coins: int
    resources: np.ndarray
    chain_symbol: int = -1
