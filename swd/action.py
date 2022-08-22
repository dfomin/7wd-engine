from dataclasses import dataclass

from swd.board_card import BoardCard
from swd.cards import Card
from swd.progress_tokens import ProgressToken
from swd.wonders import Wonder


@dataclass
class Action:
    pass


@dataclass
class BuyCardAction(Action):
    board_card: BoardCard

    @property
    def card(self) -> Card:
        return self.board_card.card


@dataclass
class DiscardCardAction(Action):
    board_card: BoardCard

    @property
    def card(self) -> Card:
        return self.board_card.card


@dataclass
class DestroyCardAction(Action):
    card: Card


@dataclass
class PickWonderAction(Action):
    wonder: Wonder


@dataclass
class BuildWonderAction(Action):
    wonder: Wonder
    board_card: BoardCard


@dataclass
class PickStartPlayerAction(Action):
    player_index: int


@dataclass
class PickProgressTokenAction(Action):
    progress_token: ProgressToken


@dataclass
class PickDiscardedCardAction(Action):
    card: Card
