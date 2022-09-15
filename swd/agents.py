import random
from abc import ABC, abstractmethod
from typing import Sequence, List, Dict, Any

from .action import Action, BuyCardAction, DiscardCardAction, DestroyCardAction, PickWonderAction, BuildWonderAction, \
    PickStartPlayerAction, PickProgressTokenAction, PickDiscardedCardAction
from .game import Game


class Agent(ABC):
    @abstractmethod
    def choose_action(self, game: Game, possible_actions: Sequence[Action]) -> Action:
        raise NotImplementedError

    def on_action_applied(self, action: Action, game: Game):
        pass


class RandomAgent(Agent):
    def choose_action(self, game: Game, possible_actions: Sequence[Action]) -> Action:
        return random.choice(possible_actions)


class RecordedAgent(Agent):
    actions: List[Dict[str, Any]]

    def __init__(self, actions: List[Dict[str, Any]]):
        super().__init__()
        self.actions = actions

    def choose_action(self, game: Game, possible_actions: Sequence[Action]) -> Action:
        action_data = self.actions.pop(0)
        for action in possible_actions:
            if type(action) == action_data["type"]:
                if isinstance(action, BuyCardAction):
                    if action_data["card_id"] == action.card.id:
                        return action
                elif isinstance(action, DiscardCardAction):
                    if action_data["card_id"] == action.card.id:
                        return action
                elif isinstance(action, DestroyCardAction):
                    if action_data["card_id"] == action.card.id:
                        return action
                elif isinstance(action, PickWonderAction):
                    if action_data["wonder_id"] == action.wonder.id:
                        return action
                elif isinstance(action, BuildWonderAction):
                    if action_data["wonder_id"] == action.wonder.id and action_data["card_id"] == action.card.id:
                        return action
                elif isinstance(action, PickStartPlayerAction):
                    if action_data["player_index"] == action.player_index:
                        return action
                elif isinstance(action, PickProgressTokenAction):
                    if action_data["token_id"] == action.progress_token.id:
                        return action
                elif isinstance(action, PickDiscardedCardAction):
                    if action_data["card_id"] == action.card.id:
                        return action
                else:
                    raise ValueError

        raise ValueError


class ConsoleAgent(Agent):
    def choose_action(self, game: Game, possible_actions: Sequence[Action]) -> Action:
        for i, action in enumerate(possible_actions):
            print(f"{i}: {action}")
        while True:
            try:
                index = int(input())
                if 0 <= index < len(possible_actions):
                    return possible_actions[index]
            except ValueError as e:
                print(e)
