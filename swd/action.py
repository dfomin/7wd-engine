from dataclasses import dataclass
from typing import Tuple


@dataclass
class Action:
    pass


@dataclass
class BuyCardAction(Action):
    card_id: int
    pos: Tuple[int, int]


@dataclass
class DiscardCardAction(Action):
    card_id: int
    pos: Tuple[int, int]


@dataclass
class DestroyCardAction(Action):
    card_id: int


@dataclass
class PickWonderAction(Action):
    wonder_id: int


@dataclass
class BuildWonderAction(Action):
    wonder_id: int
    card_id: int
    pos: Tuple[int, int]


@dataclass
class PickStartPlayerAction(Action):
    player_index: int


@dataclass
class PickProgressTokenAction(Action):
    progress_token: str


@dataclass
class PickDiscardedCardAction(Action):
    card_id: int
