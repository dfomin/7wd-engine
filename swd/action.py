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

    def __str__(self) -> str:
        return f"Buy {self.board_card.card}"


@dataclass
class DiscardCardAction(Action):
    board_card: BoardCard

    @property
    def card(self) -> Card:
        return self.board_card.card

    def __str__(self) -> str:
        return f"Discard {self.board_card.card}"


@dataclass
class DestroyCardAction(Action):
    card: Card

    def __str__(self) -> str:
        return f"Destroy {self.card}"


@dataclass
class PickWonderAction(Action):
    wonder: Wonder

    def __str__(self) -> str:
        return f"{self.wonder}"


@dataclass
class BuildWonderAction(Action):
    wonder: Wonder
    board_card: BoardCard

    def __str__(self) -> str:
        return f"Build {self.wonder} with {self.board_card.card}"


@dataclass
class PickStartPlayerAction(Action):
    player_index: int

    def __str__(self) -> str:
        return f"Start player {self.player_index}"


@dataclass
class PickProgressTokenAction(Action):
    progress_token: ProgressToken

    def __str__(self) -> str:
        return f"Pick token {self.progress_token}"


@dataclass
class PickDiscardedCardAction(Action):
    card: Card

    def __str__(self) -> str:
        return f"Pick discarded {self.card}"
