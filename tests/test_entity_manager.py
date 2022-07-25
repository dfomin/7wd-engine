from swd.entity_manager import EntityManager


def test_cards_count():
    assert EntityManager.cards_count() == 73


def test_wonders_count():
    assert EntityManager.wonders_count() == 12


def test_progress_tokens_count():
    assert EntityManager.progress_tokens_count() == 10
