from typing import Dict, Any

from .entity import Entity


class ProgressToken(Entity):
    def __init__(self, description: Dict[str, Any]):
        description["effect"]["progress_tokens"] = 1

        super().__init__(description)

    def __str__(self) -> str:
        return f"{self.name}"
