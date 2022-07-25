from swd.entity_manager import EntityManager


def test_wonder_0():
    wonder = EntityManager.wonder(0)
    print(wonder.double_turn)
    assert wonder.double_turn
