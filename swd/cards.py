from typing import Dict, Any

from .entity import Entity
from .price import Price


class Card(Entity):
    price: Price

    def __init__(self, description: Dict[str, Any]):
        description["effect"]["color"] = description["color"]

        super().__init__(description)

        self.price = Price(description["price"])

    @property
    def is_blue(self) -> bool:
        return self.has_bonus("blue")
