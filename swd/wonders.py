from typing import Dict, Any, Optional

from .cards import Card
from .entity import Entity
from .price import Price


class Wonder(Entity):
    price: Price
    card: Optional[Card] = None

    def __init__(self, description: Dict[str, Any]):
        description["effect"]["wonders"] = 1

        super().__init__(description)

        self.price = Price(description["price"])
        self.card = None

    @property
    def is_built(self):
        return self.card is not None

    @property
    def double_turn(self):
        return self.has_bonus("double_turn")

    def __str__(self) -> str:
        return f"{self.name}"
