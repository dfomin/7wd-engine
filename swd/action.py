from dataclasses import dataclass

from swd.cards import Card
from swd.progress_tokens import ProgressToken
from swd.wonders import Wonder


@dataclass
class Action:
    pass


@dataclass
class BuyCardAction(Action):
    card: Card

    def __str__(self) -> str:
        return f"Buy {self.card}"


@dataclass
class DiscardCardAction(Action):
    card: Card

    def __str__(self) -> str:
        return f"Discard {self.card}"


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
    card: Card

    def __str__(self) -> str:
        return f"Build {self.wonder} with {self.card}"


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
