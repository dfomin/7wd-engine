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
    _cards_description = None
    _wonders_description = None
    _tokens_description = None

    @classmethod
    def _load_cards(cls):
        cls._cards_description = yaml.safe_load(pkg_resources.read_text(resources, CARDS_DESCRIPTION_PATH))

    @classmethod
    def _load_wonders(cls):
        cls._wonders_description = yaml.safe_load(pkg_resources.read_text(resources, WONDERS_DESCRIPTION_PATH))

    @classmethod
    def _load_progress_tokens(cls):
        cls._tokens_description = yaml.safe_load(pkg_resources.read_text(resources, TOKENS_DESCRIPTION_PATH))

    @classmethod
    def card(cls, card_id: int) -> Card:
        if cls._cards_description is None:
            cls._load_cards()
        return Card(cls._cards_description[card_id])

    @classmethod
    def cards_count(cls) -> int:
        if cls._cards_description is None:
            cls._load_cards()
        return len(cls._cards_description)

    @classmethod
    def wonder(cls, wonder_id: int) -> Wonder:
        if cls._wonders_description is None:
            cls._load_wonders()
        return Wonder(cls._wonders_description[wonder_id])

    @classmethod
    def wonders_count(cls) -> int:
        if cls._wonders_description is None:
            cls._load_wonders()
        return len(cls._wonders_description)

    @classmethod
    def progress_token(cls, token_id: int) -> ProgressToken:
        if cls._tokens_description is None:
            cls._load_progress_tokens()
        return ProgressToken(cls._tokens_description[token_id])

    @classmethod
    def progress_tokens_count(cls) -> int:
        if cls._tokens_description is None:
            cls._load_progress_tokens()
        return len(cls._tokens_description)
