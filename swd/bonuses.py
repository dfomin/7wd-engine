from typing import Dict, Any, Tuple, List
from enum import Enum

import numpy as np


RESOURCES = [
    "wood",
    "clay",
    "stone",
    "glass",
    "paper"
]


GENERAL_RESOURCES = [
    "materials",
    "goods"
]


TRADE_RESOURCES = [
    "wood_trade",
    "clay_trade",
    "stone_trade",
    "glass_trade",
    "paper_trade"
]


CHAIN_SYMBOLS = [
    "horseshoe",
    "sword",
    "tower",
    "target",
    "helmet",
    "book",
    "gear",
    "harp",
    "teapot",
    "mask",
    "column",
    "moon",
    "sun",
    "drop",
    "temple",
    "vase",
    "barrel"
]


SCIENTIFIC_SYMBOLS = [
    "armillary_sphere",
    "wheel",
    "sundial",
    "mortar_and_pestle",
    "plumb",
    "feather",
    "law"
]


POINTS = [
    "points",
    "blue_points"
]


WONDERS = [
    "wonders"
]


POINTS_BONUS = [
    "blue_max_points",
    "brown_gray_max_points",
    "coins_max_points",
    "green_max_points",
    "red_max_points",
    "wonders_max_points",
    "yellow_max_points",
    "progress_tokens_points"
]


CARD_COLOR = [
    "brown",
    "gray",
    "blue",
    "green",
    "yellow",
    "red",
    "purple"
]


PROGRESS_TOKENS_BONUSES = [
    "architecture",
    "economy",
    "masonry",
    "strategy",
    "theology",
    "urbanism",
    "progress_tokens"
]


BONUSES = RESOURCES + GENERAL_RESOURCES + TRADE_RESOURCES + CHAIN_SYMBOLS + SCIENTIFIC_SYMBOLS + POINTS + WONDERS +\
          POINTS_BONUS + CARD_COLOR + PROGRESS_TOKENS_BONUSES
BONUSES_LIST = [RESOURCES, GENERAL_RESOURCES, TRADE_RESOURCES, CHAIN_SYMBOLS, SCIENTIFIC_SYMBOLS, POINTS, WONDERS,
                POINTS_BONUS, CARD_COLOR, PROGRESS_TOKENS_BONUSES]
PLAYER_INVALIDATE_CACHE_BONUSES = RESOURCES + GENERAL_RESOURCES + TRADE_RESOURCES + CHAIN_SYMBOLS + \
                                  ["architecture", "masonry", "urbanism"]
OPPONENT_INVALIDATE_CACHE_BONUSES = RESOURCES


def _generate_bonus_range(index: int):
    value = 0
    for i in range(index):
        value += len(BONUSES_LIST[i])
    return np.arange(value, value + len(BONUSES_LIST[index]))


PLAYER_INVALIDATE_CACHE_RANGE = np.array([x for x in range(len(BONUSES)) if BONUSES[x] in PLAYER_INVALIDATE_CACHE_BONUSES])
OPPONENT_INVALIDATE_CACHE_RANGE = np.array([x for x in range(len(BONUSES)) if BONUSES[x] in OPPONENT_INVALIDATE_CACHE_BONUSES])


INSTANT_BONUSES = [
    "coins",
    "shield",
    "brown_coins",
    "gray_coins",
    "red_coins",
    "yellow_coins",
    "wonders_coins",
    "blue_max_coins",
    "brown_gray_max_coins",
    "green_max_coins",
    "red_max_coins",
    "yellow_max_coins",
    "opponent_coins",
    "double_turn",
    "destroy_brown",
    "destroy_gray",
    "select_progress_token",
    "select_discarded"
]


class BonusManager:
    @staticmethod
    def from_dict(description: Dict[str, Any]) -> Tuple[Dict[int, int], Dict[int, int]]:
        bonuses = {}
        instant_bonuses = {}
        for effect_name, effect in description.items():
            if effect_name in BONUSES:
                bonuses[BONUSES.index(effect_name)] = effect
            elif effect_name in INSTANT_BONUSES:
                instant_bonuses[INSTANT_BONUSES.index(effect_name)] = effect
            elif effect in BONUSES:
                bonuses[BONUSES.index(effect)] = 1
            else:
                print(description, effect_name, effect)
                raise ValueError
        return bonuses, instant_bonuses

    @staticmethod
    def get_bonus(bonus: str, bonuses: Dict[int, int]) -> int:
        return bonuses.get(BONUSES.index(bonus), 0)

    @staticmethod
    def get_instant_bonus(bonus: str, instant_bonuses: Dict[int, int]) -> int:
        return instant_bonuses.get(INSTANT_BONUSES.index(bonus), 0)

    @staticmethod
    def has_bonus(bonus: str, bonuses: Dict[int, int]) -> bool:
        return bonuses.get(BONUSES.index(bonus), 0) > 0

    @staticmethod
    def scientific_bonuses_count(bonuses: Dict[int, int]) -> int:
        return len([x for x in SCIENTIFIC_SYMBOLS if BONUSES.index(x) in bonuses])

    @staticmethod
    def scientific_doubles_count(bonuses: Dict[int, int]) -> int:
        return len([x for x in SCIENTIFIC_SYMBOLS if bonuses.get(BONUSES.index(x), 0) == 2])

    @staticmethod
    def purple_bonus(bonuses_list: List[Dict[int, int]]) -> List[int]:
        purple_points = [0] * len(bonuses_list)
        purple_color_map = {
            "blue_max_points": ["blue"],
            "brown_gray_max_points": ["brown", "gray"],
            "green_max_points": ["green"],
            "red_max_points": ["red"],
            "yellow_max_points": ["yellow"],
        }
        for bonus in POINTS_BONUS:
            for i in range(len(bonuses_list)):
                if bonus in purple_color_map:
                    if bonus in bonuses_list[i]:
                        if bonus in purple_color_map:
                            for color in purple_color_map[bonus]:
                                purple_points[i] += max([x[BONUSES.index(color)] for x in bonuses_list])
                        elif bonus == "coins_max_points":
                            purple_points[i] += max([bonuses[BONUSES.index("coins")] // 3 for bonuses in bonuses_list])
                        elif bonus == "wonder_max_points":
                            purple_points[i] += 2 * max([bonuses[BONUSES.index("wonders")] for bonuses in bonuses_list])
                        else:
                            raise ValueError
        return purple_points
