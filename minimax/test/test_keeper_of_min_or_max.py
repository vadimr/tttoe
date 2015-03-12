import pytest
from minimax.keeper_of_min_or_max import KeeperOfMinOrMax

def test_keeper_of_min():
    keeper = KeeperOfMinOrMax.min()

    assert keeper.value() == None
    assert keeper.payload() == None

    keeper.check_keep_or_reject(7)
    keeper.check_keep_or_reject(8)
    keeper.check_keep_or_reject(9, "some str")

    assert keeper.value() == 7
    assert keeper.payload() == None

    keeper.check_keep_or_reject(5, "expected_payload")

    assert keeper.value() == 5
    assert keeper.payload() == "expected_payload"

def test_keeper_of_max():
    keeper = KeeperOfMinOrMax.max()

    assert keeper.value() == None
    assert keeper.payload() == None

    keeper.check_keep_or_reject(5)
    keeper.check_keep_or_reject(4)
    keeper.check_keep_or_reject(3, "some str")

    assert keeper.value() == 5
    assert keeper.payload() == None

    keeper.check_keep_or_reject(7, "expected_payload")

    assert keeper.value() == 7
    assert keeper.payload() == "expected_payload"
