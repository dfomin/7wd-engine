import random
from enum import Enum, auto
from typing import List, Optional, Dict, Any, Tuple

from .board_card import BoardCard
from .entity_manager import EntityManager
from .action import PickWonderAction, Action, PickStartPlayerAction, DiscardCardAction, BuyCardAction, \
    BuildWonderAction, PickProgressTokenAction, DestroyCardAction, PickDiscardedCardAction
from .cards import Card
from .cards_board import CardsBoard
from .military_track import MilitaryTrack
from .player import Player
from .bonuses import BONUSES, PLAYER_INVALIDATE_CACHE_RANGE, OPPONENT_INVALIDATE_CACHE_RANGE, INSTANT_BONUSES, \
    BonusManager
from .progress_tokens import ProgressToken
from .wonders import Wonder


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


class Game:
    age: int
    current_player_index: int
    progress_tokens: List[ProgressToken]
    rest_progress_tokens: List[ProgressToken]
    discard_pile: List[Card]
    is_double_turn: bool
    wonders: List[Wonder]
    players: List[Player]
    military_track: MilitaryTrack
    game_status: GameStatus
    winner: Optional[int]
    cards_board: CardsBoard
    meta_info: Dict[str, Any]
    price_cache: Optional[Dict[int, Dict[int, int]]]

    def __init__(self):
        self.age = 0
        self.current_player_index = 0

        tokens = [EntityManager.progress_token(x) for x in range(EntityManager.progress_tokens_count())]
        random.shuffle(tokens)
        self.progress_tokens = tokens[:5]
        self.rest_progress_tokens = tokens[5:]

        wonders = [EntityManager.wonder(x) for x in range(EntityManager.wonders_count())]
        random.shuffle(wonders)
        self.wonders = wonders[:8]

        self.discard_pile = []
        self.is_double_turn = False
        self.players = [Player(0), Player(1)]
        self.military_track = MilitaryTrack()
        self.game_status = GameStatus.PICK_WONDER
        self.winner = None
        self.cards_board = CardsBoard()
        self.meta_info = {}
        self.price_cache = None

    def __str__(self) -> str:
        result = ""
        card_places = self.cards_board.card_places
        max_row_length = max([len(x) for x in card_places]) if len(card_places) > 0 else 0
        for row in card_places:
            result += " " * 2 * (max_row_length - len(row))
            result += "  ".join([f"{board_card}" for board_card in row]) + "\n"
        return result

    @property
    def is_finished(self) -> bool:
        return self.game_status == GameStatus.FINISHED

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    @property
    def opponent(self) -> Player:
        return self.players[1 - self.current_player_index]

    def check_end_game(self) -> Optional[int]:
        if self.game_status not in [GameStatus.NORMAL_TURN, GameStatus.FINISHED]:
            return None

        for i, player in enumerate(self.players):
            if player.scientific_symbols_count >= 6:
                return i

        supremacist = self.military_track.military_supremacist
        if supremacist is not None:
            return supremacist

        if self.age == 2 and len(self.cards_board.available_cards()) == 0:
            (points_0, blue_points_0), points_1, blue_points_1 = self.points()
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

    def finish_game(self):
        self.game_status = GameStatus.FINISHED

    def get_available_actions(self):
        available_actions = []

        if self.game_status == GameStatus.PICK_WONDER:
            if len(self.wonders) > 4:
                available_actions = [PickWonderAction(x) for x in self.wonders[:-4]]
            else:
                available_actions = [PickWonderAction(x) for x in self.wonders]
        elif self.game_status == GameStatus.NORMAL_TURN:
            available_actions = self.available_normal_actions()
        elif self.game_status == GameStatus.PICK_START_PLAYER:
            available_actions = [PickStartPlayerAction(x) for x in range(2)]
        elif self.game_status == GameStatus.PICK_PROGRESS_TOKEN:
            available_actions = [PickProgressTokenAction(x) for x in self.progress_tokens]
        elif self.game_status == GameStatus.PICK_REST_PROGRESS_TOKEN:
            available_actions = [PickProgressTokenAction(x) for x in self.rest_progress_tokens[:3]]
        elif self.game_status == GameStatus.DESTROY_BROWN:
            opponent = self.opponent
            for card in opponent.cards:
                if card.is_brown:
                    available_actions.append(DestroyCardAction(card))
        elif self.game_status == GameStatus.DESTROY_GRAY:
            opponent = self.opponent
            for card in opponent.cards:
                if card.is_gray:
                    available_actions.append(DestroyCardAction(card))
        elif self.game_status == GameStatus.SELECT_DISCARDED:
            available_actions = [PickDiscardedCardAction(x) for x in self.discard_pile]
        elif self.game_status == GameStatus.FINISHED:
            pass
        else:
            raise ValueError
        return available_actions

    def apply_military_tokens(self, player_index: int, coins: int):
        player = self.players[player_index]
        player.coins = max(player.coins + coins, 0)

    def available_normal_actions(self) -> List[Action]:
        player = self.current_player
        board_cards = self.cards_board.available_cards()
        result: List[Action] = [DiscardCardAction(board_card) for board_card in board_cards]
        result.extend([BuyCardAction(board_card)
                       for board_card in board_cards
                       if self.card_price(board_card.card, self.current_player_index) < player.coins])

        result.extend([BuildWonderAction(wonder, board_card)
                       for board_card in board_cards
                       for wonder in player.wonders
                       if not wonder.is_built and self.wonder_price(wonder, self.current_player_index) < player.coins])

        return result

    def apply_action(self, action: Action):
        player = self.current_player
        opponent = self.opponent
        if isinstance(action, BuyCardAction):
            self.cards_board.take_card(action.board_card)
            self.buy_card(action.card)
        elif isinstance(action, DiscardCardAction):
            self.cards_board.take_card(action.board_card)
            self.discard_pile.append(action.card)
            player.coins += player.discard_bonus
        elif isinstance(action, DestroyCardAction):
            opponent.destroy_card(action.card)
            self.discard_pile.append(action.card)
            self.check_cache(action.card.bonuses, 1 - self.current_player_index)
            self.game_status = GameStatus.NORMAL_TURN
        elif isinstance(action, PickWonderAction):
            if len(self.wonders) > 4:
                if action.wonder not in self.wonders[:-4]:
                    raise ValueError
            else:
                if action.wonder not in self.wonders:
                    raise ValueError
            player.add_wonder(action.wonder)
            self.wonders.remove(action.wonder)
            if len(self.wonders) == 0:
                self.game_status = GameStatus.NORMAL_TURN
                self.current_player_index = 0
            else:
                player_index = [0, 1, 1, 0, 1, 0, 0, 1][8 - len(self.wonders)]
                self.current_player_index = player_index
        elif isinstance(action, BuildWonderAction):
            self.cards_board.take_card(action.board_card)
            if player.has_theology:
                self.is_double_turn = True
            self.build_wonder(action.wonder, action.board_card)
        elif isinstance(action, PickStartPlayerAction):
            self.current_player_index = 1 - action.player_index        # will be changed to opposite later
            self.game_status = GameStatus.NORMAL_TURN
        elif isinstance(action, PickProgressTokenAction):
            player.add_progress_token(action.progress_token)
            self.apply_instant_bonuses(self.current_player_index, action.progress_token.instant_bonuses, False)
            if action.progress_token in self.progress_tokens:
                self.progress_tokens.remove(action.progress_token)
            elif action.progress_token in self.rest_progress_tokens:
                self.rest_progress_tokens.remove(action.progress_token)
            else:
                raise ValueError
            self.check_cache(action.progress_token.bonuses, self.current_player_index)
            self.game_status = GameStatus.NORMAL_TURN
        elif isinstance(action, PickDiscardedCardAction):
            self.add_card(player, action.card)
            if self.game_status == GameStatus.SELECT_DISCARDED:
                self.game_status = GameStatus.NORMAL_TURN

        self.winner = self.check_end_game()
        if self.winner is not None:
            self.finish_game()

        if self.game_status == GameStatus.NORMAL_TURN:
            if len(self.cards_board.card_places) == 0:
                self.age = 0
                self.current_player_index = 0
                self.cards_board.generate_age(self.age)
            elif len(self.cards_board.available_cards()) == 0:
                self.age += 1
                self.cards_board.generate_age(self.age)
                self.is_double_turn = False
                if self.military_track.weaker_player is not None:
                    self.current_player_index = self.military_track.weaker_player
                    self.game_status = GameStatus.PICK_START_PLAYER
                # else:
                #     state.game_status = GameStatus.PICK_START_PLAYER
            else:
                if not self.is_double_turn:
                    self.current_player_index = 1 - self.current_player_index
                self.is_double_turn = False

    def points(self) -> List[Tuple[int, int]]:
        points = [player.bonus_points for player in self.players]
        blue_points = [player.blue_points for player in self.players]
        military_points = self.military_track.points()
        purple_points = BonusManager.purple_bonus([player.bonuses for player in self.players])

        return [(points[i] + military_points[i] + purple_points[i], blue_points[i]) for i in range(len(self.players))]

    def buy_card(self, card: Card):
        player = self.current_player
        opponent = self.opponent

        price = self.card_price(card, self.current_player_index)
        if price > player.coins:
            raise ValueError
        player.coins -= price
        if opponent.has_economy and price > 0:
            opponent.coins += (price - card.price.coins)
        self.add_card(player, card)

    def add_card(self, player: Player, card: Card):
        scientific_doubles_count = player.scientific_doubles_count
        player.add_card(card)
        self.apply_instant_bonuses(player.index, card.instant_bonuses, True)
        if scientific_doubles_count != player.scientific_doubles_count:
            if len(self.progress_tokens) > 0:
                self.game_status = GameStatus.PICK_PROGRESS_TOKEN

        self.check_cache(card.bonuses, self.current_player_index)

    def build_wonder(self, wonder: Wonder, board_card: BoardCard):
        player = self.current_player
        opponent = self.opponent
        price = self.wonder_price(wonder, self.current_player_index)
        if price > player.coins:
            raise ValueError
        player.coins -= price
        if opponent.has_economy:
            opponent.coins += (price - wonder.price.coins)
        player.build_wonder(wonder, board_card.card)
        self.apply_instant_bonuses(self.current_player_index, wonder.instant_bonuses, False)

        if player.built_wonders + opponent.built_wonders == 7:
            player.remove_unbuilt_wonders()
            opponent.remove_unbuilt_wonders()

        self.check_cache(wonder.bonuses, self.current_player_index)

    def apply_instant_bonuses(self, player_index: int, instant_bonuses: Dict[int, int], is_card: bool):
        player = self.current_player
        opponent = self.opponent
        for bonus, value in instant_bonuses.items():
            if value == 0:
                continue
            if bonus == INSTANT_BONUSES.index("coins"):
                player.coins += value
            elif bonus == INSTANT_BONUSES.index("shield"):
                if is_card and player.has_strategy:
                    value += 1
                self.military_track.apply_shields(player_index, value, lambda x, y: self.apply_military_tokens(x, y))
            elif bonus == INSTANT_BONUSES.index("brown_coins"):
                player.coins += value * player.brown_cards
            elif bonus == INSTANT_BONUSES.index("gray_coins"):
                player.coins += value * player.gray_cards
            elif bonus == INSTANT_BONUSES.index("red_coins"):
                player.coins += value * player.red_cards
            elif bonus == INSTANT_BONUSES.index("yellow_coins"):
                player.coins += value * player.yellow_cards
            elif bonus == INSTANT_BONUSES.index("wonder_coins"):
                player.coins += value * player.built_wonders
            elif bonus == INSTANT_BONUSES.index("blue_max_coins"):
                player.coins += value * max(x.blue_cards for x in self.players)
            elif bonus == INSTANT_BONUSES.index("brown_gray_max_coins"):
                player.coins += value * max(x.brown_cards + x.gray_cards for x in self.players)
            elif bonus == INSTANT_BONUSES.index("green_max_coins"):
                player.coins += value * max(x.green_cards for x in self.players)
            elif bonus == INSTANT_BONUSES.index("red_max_coins"):
                player.coins += value * max(x.red_cards for x in self.players)
            elif bonus == INSTANT_BONUSES.index("yellow_max_coins"):
                player.coins += value * max(x.yellow_cards for x in self.players)
            elif bonus == INSTANT_BONUSES.index("opponent_coins"):
                opponent.coins = max(opponent.coins + value, 0)
            elif bonus == INSTANT_BONUSES.index("double_turn"):
                self.is_double_turn = True
            elif bonus == INSTANT_BONUSES.index("destroy_brown"):
                if opponent.bonuses[BONUSES.index("brown")] > 0:
                    self.game_status = GameStatus.DESTROY_BROWN
            elif bonus == INSTANT_BONUSES.index("destroy_gray"):
                if opponent.bonuses[BONUSES.index("gray")] > 0:
                    self.game_status = GameStatus.DESTROY_GRAY
            elif bonus == INSTANT_BONUSES.index("select_progress_token"):
                random.shuffle(self.rest_progress_tokens)
                self.game_status = GameStatus.PICK_REST_PROGRESS_TOKEN
            elif bonus == INSTANT_BONUSES.index("select_discarded"):
                if len(self.discard_pile) > 0:
                    self.game_status = GameStatus.SELECT_DISCARDED

    def card_price(self, card: Card, player_index: int) -> int:
        player = self.current_player
        opponent = self.opponent

        price = None
        if self.price_cache is not None:
            price = self.price_cache.get(player_index, {}).get(card.id, None)
        if price is None:
            price = player.card_price(card, opponent.bonuses)
            if self.price_cache is not None:
                if player_index not in self.price_cache:
                    self.price_cache[player_index] = {}
                self.price_cache[player_index][card.id] = price

        return price

    def wonder_price(self, wonder: Wonder, player_index: int) -> int:
        player = self.current_player
        opponent = self.opponent

        price = None
        if self.price_cache is not None:
            price = self.price_cache.get(player_index, {}).get(EntityManager.cards_count() + wonder.id, None)
        if price is None:
            price = player.wonder_price(wonder, opponent.bonuses)
            if self.price_cache is not None:
                if player_index not in self.price_cache:
                    self.price_cache[player_index] = {}
                self.price_cache[player_index][EntityManager.cards_count() + wonder.id] = price

        return price

    def check_cache(self, bonuses: Dict[int, int], player_index: int):
        if self.price_cache is None:
            return

        if any(key in bonuses for key in PLAYER_INVALIDATE_CACHE_RANGE):
            self.price_cache[player_index] = {}
        if any(key in bonuses for key in OPPONENT_INVALIDATE_CACHE_RANGE):
            self.price_cache[1 - player_index] = {}
