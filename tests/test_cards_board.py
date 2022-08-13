from swd.cards_board import CardsBoard


def test_cards_board_age_1():
    board = CardsBoard()
    board.generate_age(0)
    assert len(board.card_places) == 5
    assert len(board.card_places[0]) == 2
    assert len(board.card_places[1]) == 3
    assert len(board.card_places[2]) == 4
    assert len(board.card_places[3]) == 5
    assert len(board.card_places[4]) == 6


def test_cards_board_age_2():
    board = CardsBoard()
    board.generate_age(1)
    assert len(board.card_places) == 5
    assert len(board.card_places[0]) == 6
    assert len(board.card_places[1]) == 5
    assert len(board.card_places[2]) == 4
    assert len(board.card_places[3]) == 3
    assert len(board.card_places[4]) == 2


def test_cards_board_age_3():
    board = CardsBoard()
    board.generate_age(2)
    assert len(board.card_places) == 7
    assert len(board.card_places[0]) == 2
    assert len(board.card_places[1]) == 3
    assert len(board.card_places[2]) == 4
    assert len(board.card_places[3]) == 2
    assert len(board.card_places[4]) == 4
    assert len(board.card_places[5]) == 3
    assert len(board.card_places[6]) == 2

    purple_count = 0
    for row in board.card_places:
        for board_card in row:
            if board_card.is_purple_back:
                purple_count += 1
    assert purple_count == 3


def test_opening_cards_age_1():
    board = CardsBoard()
    board.generate_age(0)

    assert len(board.available_cards()) == 6

    board.take_card(board.available_cards()[0])

    assert len(board.available_cards()) == 5

    board.take_card(board.available_cards()[0])

    assert len(board.available_cards()) == 5


def test_opening_cards_age_2():
    board = CardsBoard()
    board.generate_age(1)

    assert len(board.available_cards()) == 2

    available_cards = board.available_cards()
    board.take_card(available_cards[0])

    assert len(board.available_cards()) == 2

    board.take_card(available_cards[1])

    assert len(board.available_cards()) == 3


def test_opening_cards_age_3():
    board = CardsBoard()
    board.generate_age(2)

    assert len(board.available_cards()) == 2

    board.take_card(board.available_cards()[0])

    assert len(board.available_cards()) == 2
