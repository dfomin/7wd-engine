from typing import Optional, List, Tuple

from swd.cards import Card


class BoardCard:
    row: int
    column: int
    card: Optional[Card]
    is_purple_back: Optional[bool]
    parents: List['BoardCard']
    children: List['BoardCard']

    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column
        self.card = None
        self.is_purple_back = False
        self.parents = []
        self.children = []

    @property
    def pos(self) -> Tuple[int, int]:
        return self.row, self.column

    @property
    def is_available(self) -> bool:
        return len(self.parents) == 0

    def add_parent(self, parent: 'BoardCard'):
        self.parents.append(parent)
        parent.children.append(self)
