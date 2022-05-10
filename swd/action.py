from dataclasses import dataclass
from typing import Tuple


@dataclass(slots=True)
class Action:
    pass


@dataclass(slots=True)
class BuyCardAction(Action):
    card_id: int
    pos: Tuple[int, int]


@dataclass(slots=True)
class DiscardCardAction(Action):
    card_id: int
    pos: Tuple[int, int]


@dataclass(slots=True)
class DestroyCardAction(Action):
    card_id: int


@dataclass(slots=True)
class PickWonderAction(Action):
    wonder_id: int


@dataclass(slots=True)
class BuildWonderAction(Action):
    wonder_id: int
    card_id: int
    pos: Tuple[int, int]


@dataclass(slots=True)
class PickStartPlayerAction(Action):
    player_index: int


@dataclass(slots=True)
class PickProgressTokenAction(Action):
    progress_token: str


@dataclass(slots=True)
class PickDiscardedCardAction(Action):
    card_id: int
