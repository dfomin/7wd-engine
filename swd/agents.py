import random
from abc import ABC, abstractmethod
from typing import Sequence, List

from .action import Action
from .states.game_state import GameState


class Agent(ABC):
    @abstractmethod
    def choose_action(self, state: GameState, possible_actions: Sequence[Action]) -> Action:
        raise NotImplementedError


class RandomAgent(Agent):
    def choose_action(self, state: GameState, possible_actions: Sequence[Action]) -> Action:
        return random.choice(possible_actions)


class RecordedAgent(Agent):
    actions: List[Action]

    def __init__(self, actions: List[Action]):
        super().__init__()
        self.actions = actions

    def choose_action(self, state: GameState, possible_actions: Sequence[Action]) -> Action:
        return self.actions.pop(0)


class ConsoleAgent(Agent):
    def choose_action(self, state: GameState, possible_actions: Sequence[Action]) -> Action:
        for i, action in enumerate(possible_actions):
            print(f"{i}: {action}")
        while True:
            try:
                index = int(input())
                if 0 <= index < len(possible_actions):
                    return possible_actions[index]
            except ValueError as e:
                print(e)
