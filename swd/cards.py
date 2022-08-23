from typing import Dict, Any

from .entity import Entity
from .price import Price


class Card(Entity):
    price: Price

    def __init__(self, description: Dict[str, Any]):
        description["effect"]["color"] = description["color"]
        if description["color"] == "blue":
            description["effect"]["blue_points"] = description["effect"]["points"]

        super().__init__(description)

        self.price = Price(description["price"])

    @property
    def is_blue(self) -> bool:
        return self.has_bonus("blue")

    @property
    def is_brown(self) -> bool:
        return self.has_bonus("brown")

    @property
    def is_gray(self) -> bool:
        return self.has_bonus("gray")

    @property
    def is_yellow(self) -> bool:
        return self.has_bonus("yellow")

    @property
    def is_red(self) -> bool:
        return self.has_bonus("red")

    @property
    def is_green(self) -> bool:
        return self.has_bonus("green")

    def __str__(self) -> str:
        return f"{self.id} ({self.name})"
