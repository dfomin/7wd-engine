from swd.cards_board import CardsBoard


def test_age_1():
    board = CardsBoard()
    board.generate_age_1()
    assert len(board.card_places) == 5
    assert len(board.card_places[0]) == 2
    assert len(board.card_places[1]) == 3
    assert len(board.card_places[2]) == 4
    assert len(board.card_places[3]) == 5
    assert len(board.card_places[4]) == 6


def test_age_2():
    board = CardsBoard()
    board.generate_age_2()
    assert len(board.card_places) == 5
    assert len(board.card_places[0]) == 6
    assert len(board.card_places[1]) == 5
    assert len(board.card_places[2]) == 4
    assert len(board.card_places[3]) == 3
    assert len(board.card_places[4]) == 2


def test_age_3():
    board = CardsBoard()
    board.generate_age_3()
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
