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
    "points"
]


POINTS_BONUS = [
    "blue_max_points",
    "brown_gray_max_points",
    "coins_max_points",
    "green_max_points",
    "red_max_points",
    "wonder_max_points",
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
    "progress_token"
]


BONUSES = RESOURCES + GENERAL_RESOURCES + TRADE_RESOURCES + CHAIN_SYMBOLS + SCIENTIFIC_SYMBOLS + POINTS + POINTS_BONUS\
          + CARD_COLOR + PROGRESS_TOKENS_BONUSES
BONUSES_LIST = [RESOURCES, GENERAL_RESOURCES, TRADE_RESOURCES, CHAIN_SYMBOLS, SCIENTIFIC_SYMBOLS, POINTS, POINTS_BONUS,
                CARD_COLOR, PROGRESS_TOKENS_BONUSES]
PLAYER_INVALIDATE_CACHE_BONUSES = RESOURCES + GENERAL_RESOURCES + TRADE_RESOURCES + CHAIN_SYMBOLS + \
                                  ["architecture", "masonry", "urbanism"]
OPPONENT_INVALIDATE_CACHE_BONUSES = RESOURCES


def _generate_bonus_range(index: int):
    value = 0
    for i in range(index):
        value += len(BONUSES_LIST[i])
    return slice(value, value + len(BONUSES_LIST[index]))


RESOURCE_RANGE = _generate_bonus_range(0)
GENERAL_RESOURCES_RANGE = _generate_bonus_range(1)
TRADE_RESOURCES_RANGE = _generate_bonus_range(2)
CHAIN_SYMBOLS_RANGE = _generate_bonus_range(3)
SCIENTIFIC_SYMBOLS_RANGE = _generate_bonus_range(4)
POINTS_RANGE = _generate_bonus_range(5)
POINTS_BONUS_RANGE = _generate_bonus_range(6)
CARD_COLOR_RANGE = _generate_bonus_range(7)
PROGRESS_TOKENS_RANGE = _generate_bonus_range(8)
PLAYER_INVALIDATE_CACHE_RANGE = np.array([x for x in range(len(BONUSES)) if BONUSES[x] in PLAYER_INVALIDATE_CACHE_BONUSES])
OPPONENT_INVALIDATE_CACHE_RANGE = np.array([x for x in range(len(BONUSES)) if BONUSES[x] in OPPONENT_INVALIDATE_CACHE_BONUSES])


INSTANT_BONUSES = [
    "coins",
    "shield",
    "brown_coins",
    "gray_coins",
    "red_coins",
    "yellow_coins",
    "wonder_coins",
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
