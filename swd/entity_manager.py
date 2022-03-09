import importlib.resources as pkg_resources
from typing import List

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
    def card(cls, card_id: int) -> Card:
        if cls._cards is None:
            cards_description = pkg_resources.read_text(resources, CARDS_DESCRIPTION_PATH)
            cls._cards = [Card.from_dict(x) for x in yaml.safe_load(cards_description)]
        return cls._cards[card_id]

    @classmethod
    def cards_count(cls) -> int:
        if cls._cards is None:
            cards_description = pkg_resources.read_text(resources, CARDS_DESCRIPTION_PATH)
            cls._cards = [Card.from_dict(x) for x in yaml.safe_load(cards_description)]
        return len(cls._cards)

    @classmethod
    def wonder(cls, wonder_id: int) -> Wonder:
        if cls._wonders is None:
            wonders_description = pkg_resources.read_text(resources, WONDERS_DESCRIPTION_PATH)
            cls._wonders = [Wonder.from_dict(x) for x in yaml.safe_load(wonders_description)]
        return cls._wonders[wonder_id]

    @classmethod
    def wonders_count(cls) -> int:
        if cls._wonders is None:
            wonders_description = pkg_resources.read_text(resources, WONDERS_DESCRIPTION_PATH)
            cls._wonders = [Wonder.from_dict(x) for x in yaml.safe_load(wonders_description)]
        return len(cls._wonders)

    @classmethod
    def progress_token_names(cls) -> List[str]:
        if cls._tokens is None:
            tokens_description = pkg_resources.read_text(resources, TOKENS_DESCRIPTION_PATH)
            tokens = yaml.safe_load(tokens_description)
            cls._tokens = {token["name"]: ProgressToken.from_dict(token) for token in tokens}
        return list(cls._tokens.keys())

    @classmethod
    def progress_token(cls, token_name: str) -> ProgressToken:
        if cls._tokens is None:
            tokens_description = pkg_resources.read_text(resources, TOKENS_DESCRIPTION_PATH)
            tokens = yaml.safe_load(tokens_description)
            cls._tokens = {token["name"]: ProgressToken.from_dict(token) for token in tokens}
        return cls._tokens[token_name]
