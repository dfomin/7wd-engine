import random
from typing import Dict, List, Optional, Tuple

import numpy as np

from .entity_manager import EntityManager
from .action import PickWonderAction, Action, PickStartPlayerAction, DiscardCardAction, BuyCardAction, \
    BuildWonderAction, PickProgressTokenAction, DestroyCardAction, PickDiscardedCardAction
from .cards import Card
from .cards_board import CardsBoard
from .military_track import MilitaryTrack
from .player import Player
from .bonuses import InstantBonus, POINTS_BONUS_RANGE, POINTS_BONUS, BONUSES, PLAYER_INVALIDATE_CACHE_RANGE, \
    OPPONENT_INVALIDATE_CACHE_RANGE
from .states.cards_board_state import CardsBoardState
from .states.game_state import GameState, GameStatus
from .states.military_state_track import MilitaryTrackState
from .states.player_state import PlayerState
from .wonders import Wonder


class Game:
    @staticmethod
    def create() -> GameState:
        wonders = np.arange(12)
        np.random.shuffle(wonders)
        wonders = [x for x in wonders[:8]]

        tokens = EntityManager.progress_token_names()
        random.shuffle(tokens)
        progress_tokens = tokens[:5]
        rest_progress_tokens = tokens[5:]

        return GameState(0,
                         0,
                         progress_tokens,
                         rest_progress_tokens,
                         [],
                         False,
                         wonders,
                         [PlayerState(0), PlayerState(1)],
                         MilitaryTrackState(),
                         GameStatus.PICK_WONDER,
                         None,
                         CardsBoardState(0, np.array([]), np.array([]), np.array([]), None),
                         {})

    @staticmethod
    def print(state: GameState) -> str:
        result = ""
        for player_state in state.players_state:
            result += f"{player_state.coins} {Player.resources(player_state)} {Game.points(state, player_state.index)[0]}\n"
            for wonder in Player.wonders(player_state):
                result += f"{wonder.name} ({'+' if wonder.is_built else '-'})\n"
        result += f"{CardsBoard.print(state.cards_board_state)}"
        return result

    @staticmethod
    def is_finished(state: GameState):
        return state.game_status == GameStatus.FINISHED

    @staticmethod
    def check_end_game(state: GameState) -> Optional[int]:
        if state.game_status != GameStatus.NORMAL_TURN and state.game_status != GameStatus.FINISHED:
            return None
        for i, player_state in enumerate(state.players_state):
            if np.count_nonzero(Player.scientific_symbols(player_state)) >= 6:
                return i
        supremacist = MilitaryTrack.military_supremacist(state.military_track_state)
        if supremacist is not None:
            return supremacist
        if state.age == 2 and len(CardsBoard.available_cards(state.cards_board_state)) == 0:
            points_0, blue_points_0 = Game.points(state, 0)
            points_1, blue_points_1 = Game.points(state, 1)
            if points_0 > points_1:
                return 0
            elif points_0 < points_1:
                return 1
            elif blue_points_0 > blue_points_1:
                return 0
            elif blue_points_0 < blue_points_1:
                return 1
            else:
                return -1
        return None

    @staticmethod
    def finish_game(state: GameState):
        state.game_status = GameStatus.FINISHED

    @staticmethod
    def get_available_actions(state: GameState):
        available_actions = []

        if state.game_status == GameStatus.PICK_WONDER:
            if len(state.wonders) > 4:
                available_actions = [PickWonderAction(x) for x in state.wonders[:-4]]
            else:
                available_actions = [PickWonderAction(x) for x in state.wonders]
        elif state.game_status == GameStatus.NORMAL_TURN:
            available_actions = Game.available_normal_actions(state)
        elif state.game_status == GameStatus.PICK_START_PLAYER:
            available_actions = [PickStartPlayerAction(x) for x in range(2)]
        elif state.game_status == GameStatus.PICK_PROGRESS_TOKEN:
            available_actions = [PickProgressTokenAction(x) for x in state.progress_tokens]
        elif state.game_status == GameStatus.PICK_REST_PROGRESS_TOKEN:
            available_actions = [PickProgressTokenAction(x) for x in state.rest_progress_tokens[:3]]
        elif state.game_status == GameStatus.DESTROY_BROWN:
            opponent_state = state.players_state[1 - state.current_player_index]
            for card in Player.cards(opponent_state):
                if card.bonuses[BONUSES.index("brown")] > 0:
                    available_actions.append(DestroyCardAction(card.id))
        elif state.game_status == GameStatus.DESTROY_GRAY:
            opponent_state = state.players_state[1 - state.current_player_index]
            for card in Player.cards(opponent_state):
                if card.bonuses[BONUSES.index("gray")] > 0:
                    available_actions.append(DestroyCardAction(card.id))
        elif state.game_status == GameStatus.SELECT_DISCARDED:
            available_actions = [PickDiscardedCardAction(x) for x in state.discard_pile]
        elif state.game_status == GameStatus.FINISHED:
            pass
        else:
            raise ValueError
        return available_actions

    @staticmethod
    def apply_military_tokens(state: GameState, player_index: int, coins: int):
        player_state = state.players_state[player_index]
        player_state.coins = max(player_state.coins + coins, 0)

    @staticmethod
    def available_normal_actions(state: GameState) -> List[Action]:
        player_state = state.players_state[state.current_player_index]
        result: List[Action] = []
        cards = [(EntityManager.card(x[0]), x[1]) for x in CardsBoard.available_cards(state.cards_board_state)]
        result.extend([DiscardCardAction(x[0].id, x[1]) for x in cards])
        for card, pos in cards:
            price = Game.card_price(state, card, state.current_player_index)
            if price <= player_state.coins:
                result.append(BuyCardAction(card.id, pos))

        wonders_to_build = [EntityManager.wonder(x[0]) for x in player_state.wonders if x[1] is None]
        for wonder in wonders_to_build:
            price = Game.wonder_price(state, wonder, state.current_player_index)
            if price > player_state.coins:
                continue
            for card, pos in cards:
                result.append(BuildWonderAction(wonder.id, card.id, pos))

        return result

    @staticmethod
    def apply_action(state: GameState, action: Action):
        player_state = state.players_state[state.current_player_index]
        if isinstance(action, BuyCardAction):
            CardsBoard.take_card(state.cards_board_state, action.card_id)
            Game.buy_card(state, EntityManager.card(action.card_id))
        elif isinstance(action, DiscardCardAction):
            CardsBoard.take_card(state.cards_board_state, action.card_id)
            state.discard_pile.append(action.card_id)
            player_state.coins += 2 + player_state.bonuses[BONUSES.index("yellow")]
        elif isinstance(action, DestroyCardAction):
            Player.destroy_card(state.players_state[1 - state.current_player_index], action.card_id)
            state.discard_pile.append(action.card_id)
            Game.check_cache(state, EntityManager.card(action.card_id).bonuses, 1 - state.current_player_index)
            state.game_status = GameStatus.NORMAL_TURN
        elif isinstance(action, PickWonderAction):
            if len(state.wonders) > 4:
                if action.wonder_id not in state.wonders[:-4]:
                    raise ValueError
            else:
                if action.wonder_id not in state.wonders:
                    raise ValueError
            Player.add_wonder(state.players_state[state.current_player_index], action.wonder_id)
            state.wonders.remove(action.wonder_id)
            if len(state.wonders) == 0:
                state.game_status = GameStatus.NORMAL_TURN
                state.current_player_index = 0
            else:
                player_index = [0, 1, 1, 0, 1, 0, 0, 1][8 - len(state.wonders)]
                state.current_player_index = player_index
        elif isinstance(action, BuildWonderAction):
            CardsBoard.take_card(state.cards_board_state, action.card_id)
            if player_state.bonuses[BONUSES.index("theology")] > 0:
                state.is_double_turn = True
            Game.build_wonder(state, action.wonder_id, action.card_id)
        elif isinstance(action, PickStartPlayerAction):
            state.current_player_index = 1 - action.player_index        # will be changed to opposite later
            state.game_status = GameStatus.NORMAL_TURN
        elif isinstance(action, PickProgressTokenAction):
            token = EntityManager.progress_token(action.progress_token)
            Player.add_progress_token(player_state, token)
            Game.apply_instant_bonus(state, player_state.index, token.instant_bonus, True)
            if action.progress_token in state.progress_tokens:
                state.progress_tokens.remove(action.progress_token)
            elif action.progress_token in state.rest_progress_tokens:
                state.rest_progress_tokens.remove(action.progress_token)
            else:
                raise ValueError
            Game.check_cache(state, token.bonuses, state.current_player_index)
            state.game_status = GameStatus.NORMAL_TURN
        elif isinstance(action, PickDiscardedCardAction):
            Game.add_card(state, player_state, EntityManager.card(action.card_id))
            if state.game_status == GameStatus.SELECT_DISCARDED:
                state.game_status = GameStatus.NORMAL_TURN

        state.winner = Game.check_end_game(state)
        if state.winner is not None:
            Game.finish_game(state)

        if state.game_status == GameStatus.NORMAL_TURN:
            if len(state.cards_board_state.card_places) == 0:
                state.age = 0
                state.current_player_index = 0
                state.cards_board_state.age = state.age
                CardsBoard.generate_age(state.cards_board_state)
            elif len(CardsBoard.available_cards(state.cards_board_state)) == 0:
                state.age += 1
                state.cards_board_state.age += 1
                CardsBoard.generate_age(state.cards_board_state)
                state.is_double_turn = False
                if MilitaryTrack.weaker_player(state.military_track_state) is not None:
                    state.current_player_index = MilitaryTrack.weaker_player(state.military_track_state)
                    state.game_status = GameStatus.PICK_START_PLAYER
                # else:
                #     state.game_status = GameStatus.PICK_START_PLAYER
            else:
                if not state.is_double_turn:
                    state.current_player_index = 1 - state.current_player_index
                state.is_double_turn = False

    @staticmethod
    def points(state: GameState, player_index: int):
        player_state = state.players_state[player_index]
        opponent_state = state.players_state[1 - player_index]

        bonuses = state.players_state[player_index].bonuses

        player_cards = [EntityManager.card(card_id) for card_id in player_state.cards]
        player_wonders = [EntityManager.wonder(info[0]) for info in player_state.wonders if info[1] is not None]
        opponent_wonders = [EntityManager.wonder(info[0]) for info in opponent_state.wonders if info[1] is not None]
        player_tokens = [EntityManager.progress_token(name) for name in player_state.progress_tokens]

        cards = sum([card.points for card in player_cards])
        blue_cards = sum([card.points for card in player_cards if card.bonuses[BONUSES.index("blue")] > 0])
        wonders = sum([wonder.points for wonder in player_wonders])
        tokens = sum([token.points for token in player_tokens])
        coins = player_state.coins // 3
        military = MilitaryTrack.points(state.military_track_state, player_index)
        bonus_points: int = 0
        bonus_color_map = {
            POINTS_BONUS.index("blue_max_points"): ["blue"],
            POINTS_BONUS.index("brown_gray_max_points"): ["brown", "gray"],
            POINTS_BONUS.index("green_max_points"): ["green"],
            POINTS_BONUS.index("red_max_points"): ["red"],
            POINTS_BONUS.index("yellow_max_points"): ["yellow"],
        }
        for card in player_cards:
            if card.bonuses[BONUSES.index("purple")] == 0:
                continue
            for bonus in np.where(card.bonuses[POINTS_BONUS_RANGE] > 0)[0]:
                if bonus in bonus_color_map:
                    colors = bonus_color_map[bonus]
                    own_cards_count = 0
                    opponent_cards_count = 0
                    for color in colors:
                        own_cards_count += player_state.bonuses[BONUSES.index(color)]
                        opponent_cards_count += opponent_state.bonuses[BONUSES.index(color)]
                    bonus_points += max(own_cards_count, opponent_cards_count)
                elif bonus == POINTS_BONUS.index("coins_max_points"):
                    bonus_points += max(player_state.coins // 3, opponent_state.coins // 3)
                elif bonus == POINTS_BONUS.index("wonder_max_points"):
                    bonus_points += 2 * max(len(player_wonders), len(opponent_wonders))
                else:
                    raise ValueError

        bonus_points += bonuses[BONUSES.index("progress_tokens_points")] * bonuses[BONUSES.index("progress_token")]
        return cards + wonders + tokens + coins + military + bonus_points, blue_cards

    @staticmethod
    def buy_card(state: GameState, card: Card):
        player_state = state.players_state[state.current_player_index]
        opponent_state = state.players_state[1 - state.current_player_index]

        price = Game.card_price(state, card, state.current_player_index)
        if price > player_state.coins:
            raise ValueError
        player_state.coins -= price
        if opponent_state.bonuses[BONUSES.index("economy")] > 0 and price > 0:
            opponent_state.coins += (price - card.price.coins)
        Game.add_card(state, player_state, card)

    @staticmethod
    def add_card(state: GameState, player_state: PlayerState, card: Card):
        double_scientific_symbols = np.sum(Player.scientific_symbols(player_state) == 2)
        Player.add_card(player_state, card)
        Game.apply_instant_bonus(state, player_state.index, card.instant_bonus, True)
        if double_scientific_symbols != np.sum(Player.scientific_symbols(player_state) == 2):
            if len(state.progress_tokens) > 0:
                state.game_status = GameStatus.PICK_PROGRESS_TOKEN

        Game.check_cache(state, card.bonuses, state.current_player_index)

    @staticmethod
    def build_wonder(state: GameState, wonder_id: int, card_id: int):
        player_state = state.players_state[state.current_player_index]
        opponent_state = state.players_state[1 - state.current_player_index]
        wonder: Wonder = EntityManager.wonder(wonder_id)
        price = Game.wonder_price(state, wonder, state.current_player_index)
        if price > player_state.coins:
            raise ValueError
        player_state.coins -= price
        if opponent_state.bonuses[BONUSES.index("economy")] > 0:
            opponent_state.coins += (price - wonder.price.coins)
        Player.build_wonder(player_state, wonder_id, card_id)
        Game.apply_instant_bonus(state, state.current_player_index, wonder.instant_bonus, False)

        if len([x for x in player_state.wonders if x[1] is not None]) + \
                len([x for x in opponent_state.wonders if x[1] is not None]) == 7:
            Player.remove_unbuilt_wonders(player_state)
            Player.remove_unbuilt_wonders(opponent_state)

        Game.check_cache(state, wonder.bonuses, state.current_player_index)

    @staticmethod
    def apply_instant_bonus(state: GameState, player_index: int, instant_bonus: Dict[InstantBonus, int], is_card: bool):
        player_state = state.players_state[player_index]
        opponent_state = state.players_state[1 - player_index]
        for bonus, value in instant_bonus.items():
            if bonus == InstantBonus.COINS:
                player_state.coins += value
            elif bonus == InstantBonus.SHIELD:
                if is_card and player_state.bonuses[BONUSES.index("strategy")] > 0:
                    value += 1
                MilitaryTrack.apply_shields(state.military_track_state,
                                            player_index,
                                            value,
                                            lambda x, y: Game.apply_military_tokens(state, x, y))
            elif bonus == InstantBonus.BROWN_COINS:
                player_state.coins += value * player_state.bonuses[BONUSES.index("brown")]
            elif bonus == InstantBonus.GRAY_COINS:
                player_state.coins += value * player_state.bonuses[BONUSES.index("gray")]
            elif bonus == InstantBonus.RED_COINS:
                player_state.coins += value * player_state.bonuses[BONUSES.index("red")]
            elif bonus == InstantBonus.YELLOW_COINS:
                player_state.coins += value * player_state.bonuses[BONUSES.index("yellow")]
            elif bonus == InstantBonus.WONDER_COINS:
                player_state.coins += value * len([x for x in player_state.wonders if x[1] is not None])
            elif bonus == InstantBonus.BLUE_MAX_COINS:
                player_state.coins += value * max(x.bonuses[BONUSES.index("blue")] for x in state.players_state)
            elif bonus == InstantBonus.BROWN_GRAY_MAX_COINS:
                player_state.coins += value * max(x.bonuses[BONUSES.index("brown")] +
                                                  x.bonuses[BONUSES.index("gray")]
                                                  for x in state.players_state)
            elif bonus == InstantBonus.GREEN_MAX_COINS:
                player_state.coins += value * max(x.bonuses[BONUSES.index("green")] for x in state.players_state)
            elif bonus == InstantBonus.RED_MAX_COINS:
                player_state.coins += value * max(x.bonuses[BONUSES.index("red")] for x in state.players_state)
            elif bonus == InstantBonus.YELLOW_MAX_COINS:
                player_state.coins += value * max(x.bonuses[BONUSES.index("yellow")] for x in state.players_state)
            elif bonus == InstantBonus.OPPONENT_COINS:
                opponent_state.coins = max(opponent_state.coins + value, 0)
            elif bonus == InstantBonus.DOUBLE_TURN:
                state.is_double_turn = True
            elif bonus == InstantBonus.DESTROY_BROWN:
                if opponent_state.bonuses[BONUSES.index("brown")] > 0:
                    state.game_status = GameStatus.DESTROY_BROWN
            elif bonus == InstantBonus.DESTROY_GRAY:
                if opponent_state.bonuses[BONUSES.index("gray")] > 0:
                    state.game_status = GameStatus.DESTROY_GRAY
            elif bonus == InstantBonus.SELECT_PROGRESS_TOKEN:
                np.random.shuffle(state.rest_progress_tokens)
                state.game_status = GameStatus.PICK_REST_PROGRESS_TOKEN
            elif bonus == InstantBonus.SELECT_DISCARDED:
                if len(state.discard_pile) > 0:
                    state.game_status = GameStatus.SELECT_DISCARDED

    @staticmethod
    def card_price(state: GameState, card: Card, player_index: int) -> int:
        player_state = state.players_state[player_index]
        opponent_state = state.players_state[1 - player_index]

        price = None
        if state.price_cache is not None:
            price = state.price_cache.get(player_index, {}).get(card.id, None)
        if price is None:
            price = Player.card_price(player_state, card, opponent_state)
            if state.price_cache is not None:
                if player_index not in state.price_cache:
                    state.price_cache[player_index] = {}
                state.price_cache[player_index][card.id] = price

        return price

    @staticmethod
    def wonder_price(state: GameState, wonder: Wonder, player_index: int) -> int:
        player_state = state.players_state[player_index]
        opponent_state = state.players_state[1 - player_index]

        price = None
        if state.price_cache is not None:
            price = state.price_cache.get(player_index, {}).get(EntityManager.cards_count() + wonder.id, None)
        if price is None:
            price = Player.wonder_price(player_state, wonder, opponent_state)
            if state.price_cache is not None:
                if player_index not in state.price_cache:
                    state.price_cache[player_index] = {}
                state.price_cache[player_index][EntityManager.cards_count() + wonder.id] = price

        return price

    @staticmethod
    def check_cache(state: GameState, bonuses: np.ndarray, player_index: int):
        if state.price_cache is None:
            return

        if np.count_nonzero(bonuses[PLAYER_INVALIDATE_CACHE_RANGE]) > 0:
            state.price_cache[player_index] = {}
        if np.count_nonzero(bonuses[OPPONENT_INVALIDATE_CACHE_RANGE]) > 0:
            state.price_cache[1 - player_index] = {}
