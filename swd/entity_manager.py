import importlib.resources as pkg_resources

import yaml

from .cards import Card
from .progress_tokens import ProgressToken
from .wonders import Wonder

from . import resources


CARDS_DESCRIPTION_PATH = "cards.yaml"
WONDERS_DESCRIPTION_PATH = "wonders.yaml"
TOKENS_DESCRIPTION_PATH = "tokens.yaml"


class EntityManager:
    _cards = None
    _wonders = None
    _tokens = None

    @classmethod
    def _load_cards(cls):
        cards_description = pkg_resources.read_text(resources, CARDS_DESCRIPTION_PATH)
        cls._cards = [Card(x) for x in yaml.safe_load(cards_description)]

    @classmethod
    def _load_wonders(cls):
        wonders_description = pkg_resources.read_text(resources, WONDERS_DESCRIPTION_PATH)
        cls._wonders = [Wonder(x) for x in yaml.safe_load(wonders_description)]

    @classmethod
    def _load_progress_tokens(cls):
        tokens_description = pkg_resources.read_text(resources, TOKENS_DESCRIPTION_PATH)
        cls._tokens = [ProgressToken(token) for token in yaml.safe_load(tokens_description)]

    @classmethod
    def card(cls, card_id: int) -> Card:
        if cls._cards is None:
            cls._load_cards()
        return cls._cards[card_id]

    @classmethod
    def cards_count(cls) -> int:
        if cls._cards is None:
            cls._load_cards()
        return len(cls._cards)

    @classmethod
    def wonder(cls, wonder_id: int) -> Wonder:
        if cls._wonders is None:
            cls._load_wonders()
        return cls._wonders[wonder_id]

    @classmethod
    def wonders_count(cls) -> int:
        if cls._wonders is None:
            cls._load_wonders()
        return len(cls._wonders)

    @classmethod
    def progress_token(cls, token_id: int) -> ProgressToken:
        if cls._tokens is None:
            cls._load_progress_tokens()
        return cls._tokens[token_id]

    @classmethod
    def progress_tokens_count(cls) -> int:
        if cls._tokens is None:
            cls._load_progress_tokens()
        return len(cls._tokens)
