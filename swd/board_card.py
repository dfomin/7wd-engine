from typing import Optional, List, Tuple

from swd.cards import Card
from swd.entity_manager import EntityManager


class BoardCard:
    row: int
    column: int
    card: Optional[Card]
    is_purple_back: Optional[bool]
    is_taken: bool
    parents: List['BoardCard']
    children: List['BoardCard']

    def __init__(self, age: int, row: int, column: int):
        self.age = age
        self.row = row
        self.column = column
        self.card = None
        self.is_purple_back = False
        self.is_taken = False
        self.parents = []
        self.children = []

    @property
    def pos(self) -> Tuple[int, int]:
        return self.row, self.column

    @property
    def is_available(self) -> bool:
        return not self.is_taken and len(self.parents) == 0

    def add_parent(self, parent: 'BoardCard'):
        self.parents.append(parent)
        parent.children.append(self)

    def remove_parent(self, parent: 'BoardCard'):
        self.parents.remove(parent)

    def __str__(self) -> str:
        if self.is_taken:
            return "  "
        return f"{self.card.id:2d}" if self.card is not None else " ."

    def clone(self) -> 'BoardCard':
        board_card = BoardCard(self.age, self.row, self.column)
        board_card.card = EntityManager.card(self.card.id) if self.card is not None else None
        board_card.is_purple_back = self.is_purple_back
        board_card.is_taken = self.is_taken
        return board_card
