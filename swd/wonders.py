from typing import Dict, Any, Optional

from .entity import Entity
from .price import Price


class Wonder(Entity):
    price: Price
    card_id: Optional[int] = None

    def __init__(self, description: Dict[str, Any]):
        super().__init__(description)

        self.price = Price(description["price"])
        self.card_id = None

    @property
    def is_built(self):
        return self.card_id is not None

    @property
    def double_turn(self):
        return self.has_bonus("double_turn")
