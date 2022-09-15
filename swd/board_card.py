from typing import Optional, List, Tuple

from swd.cards import Card


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
        return f"{self.card.id}" if self.card is not None else " ."
