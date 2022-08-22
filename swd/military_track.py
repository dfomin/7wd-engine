from typing import Callable, Optional, List, Tuple


class MilitaryTrack:
    conflict_pawn: int
    military_tokens: List[bool]

    def __init__(self, conflict_pawn: int = 0, military_tokens: Optional[List[bool]] = None):
        if military_tokens is None:
            military_tokens = [True] * 4
        self.conflict_pawn = conflict_pawn
        self.military_tokens = military_tokens

    @property
    def military_supremacist(self) -> Optional[int]:
        if self.conflict_pawn == 9:
            return 0
        elif self.conflict_pawn == -9:
            return 1
        return None

    @property
    def weaker_player(self) -> Optional[int]:
        if self.conflict_pawn > 0:
            return 1
        elif self.conflict_pawn < 0:
            return 0
        return None

    def apply_shields(self,
                      player_index: int,
                      shields: int,
                      military_tokens_callback: Callable[[int, int], None]):
        if player_index == 1:
            shields = -shields
        self.conflict_pawn = min(max(self.conflict_pawn + shields, -9), 9)

        if self.conflict_pawn >= 3 and self.military_tokens[2]:
            self.military_tokens[2] = False
            military_tokens_callback(1, -2)
        if self.conflict_pawn >= 6 and self.military_tokens[3]:
            self.military_tokens[3] = False
            military_tokens_callback(1, -5)
        if self.conflict_pawn <= -3 and self.military_tokens[1]:
            self.military_tokens[1] = False
            military_tokens_callback(0, -2)
        if self.conflict_pawn <= -6 and self.military_tokens[0]:
            self.military_tokens[0] = False
            military_tokens_callback(0, -5)

    def points(self) -> Tuple[int, int]:
        if self.military_supremacist is not None or self.conflict_pawn == 0:
            return 0, 0
        zone_points = [2, 5, 10][abs(self.conflict_pawn) // 3]
        return (zone_points, 0) if self.conflict_pawn > 0 else (0, zone_points)

    def clone(self) -> 'MilitaryTrack':
        return MilitaryTrack(self.conflict_pawn,
                             self.military_tokens.copy())
