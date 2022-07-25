from swd.entity_manager import EntityManager


def test_card_0():
    card = EntityManager.card(0)
    assert not card.is_blue
    assert card.points == 0
