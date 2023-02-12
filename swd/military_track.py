from typing import Callable, Optional

from .states.military_state_track import MilitaryTrackState


class MilitaryTrack:
    @staticmethod
    def apply_shields(state: MilitaryTrackState,
                      player_index: int,
                      shields: int,
                      military_tokens_callback: Callable[[int, int], None]):
        if player_index == 1:
            shields = -shields
        state.conflict_pawn = min(max(state.conflict_pawn + shields, -9), 9)

        if state.conflict_pawn >= 3 and state.military_tokens[2]:
            state.military_tokens[2] = False
            military_tokens_callback(1, -2)
        if state.conflict_pawn >= 6 and state.military_tokens[3]:
            state.military_tokens[3] = False
            military_tokens_callback(1, -5)
        if state.conflict_pawn <= -3 and state.military_tokens[1]:
            state.military_tokens[1] = False
            military_tokens_callback(0, -2)
        if state.conflict_pawn <= -6 and state.military_tokens[0]:
            state.military_tokens[0] = False
            military_tokens_callback(0, -5)

    @staticmethod
    def military_supremacist(state: MilitaryTrackState) -> Optional[int]:
        if state.conflict_pawn == 9:
            return 0
        elif state.conflict_pawn == -9:
            return 1
        return None

    @staticmethod
    def weaker_player(state: MilitaryTrackState) -> Optional[int]:
        if state.conflict_pawn > 0:
            return 1
        elif state.conflict_pawn < 0:
            return 0
        return None

    @staticmethod
    def points(state: MilitaryTrackState, player_index: int) -> int:
        if MilitaryTrack.military_supremacist(state) is not None:
            return 0
        if player_index == 0 and state.conflict_pawn <= 0 or player_index == 1 and state.conflict_pawn >= 0:
            return 0
        return [2, 5, 10][abs(state.conflict_pawn) // 3]
