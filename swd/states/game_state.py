from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional, Any, Dict, Tuple

import numpy as np

from .cards_board_state import CardsBoardState
from .military_state_track import MilitaryTrackState
from .player_state import PlayerState


class GameStatus(Enum):
    PICK_WONDER = auto()
    NORMAL_TURN = auto()
    PICK_PROGRESS_TOKEN = auto()
    PICK_REST_PROGRESS_TOKEN = auto()
    PICK_START_PLAYER = auto()
    DESTROY_BROWN = auto()
    DESTROY_GRAY = auto()
    SELECT_DISCARDED = auto()
    FINISHED = auto()


@dataclass
class GameState:
    age: int
    current_player_index: int
    progress_tokens: List[str]
    rest_progress_tokens: List[str]
    discard_pile: List[int]
    is_double_turn: bool
    wonders: List[int]
    players_state: List[PlayerState]
    military_track_state: MilitaryTrackState
    game_status: GameStatus
    winner: Optional[int]
    cards_board_state: CardsBoardState
    meta_info: Dict[str, Any]
    price_cache: Optional[Dict[int, Dict[int, int]]] = None

    def clone(self) -> 'GameState':
        return GameState(self.age,
                         self.current_player_index,
                         self.progress_tokens.copy(),
                         self.rest_progress_tokens.copy(),
                         self.discard_pile.copy(),
                         self.is_double_turn,
                         self.wonders.copy(),
                         [p.clone() for p in self.players_state],
                         self.military_track_state.clone(),
                         self.game_status,
                         self.winner,
                         self.cards_board_state.clone(),
                         self.meta_info)
