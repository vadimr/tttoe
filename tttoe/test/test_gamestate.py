import pytest
from tttoe.gamestate import GameState

def test_init_default_last_step_result():
    state = GameState(3, 3, 2)
    assert state.last_move_result == "nothing"

def test_all_available_moves():
    field = [[None, "b", None, "e"],
             ["a", "c", "d", "f"],
             [None, None, None, None]]
    state = GameState(3, 4, 3, field=field)
    moves = [(pos_x, pos_y) for pos_x, pos_y in state.all_available_moves()]
    assert moves == [(0, 0), (0, 2), (2, 0), (2, 1), (2, 2), (2, 3)]

def test_make_move_validates_reserved_hanles():
    exp_message = "\"nothing\" and \"draw\" hanles are reserved"

    state = GameState(3, 2, 3)
    with pytest.raises(ValueError) as excinfo:
        state.make_move(0, 0, "nothing")
    assert str(excinfo.value) == exp_message

    with pytest.raises(ValueError) as excinfo:
        state.make_move(0, 0, "draw")
    assert str(excinfo.value) == exp_message

def test_make_move_validates_if_step_is_available():
    state = GameState(3, 2, 3, "abc   ")

    with pytest.raises(ValueError) as excinfo:
        state.make_move(0, 0, "d")

    assert str(excinfo.value) == "The value in the cell (0, 0) is already " \
        "set"

def test_make_move_results_draw():
    field = [["a", None], ["b", "e"], ["c", "f"]]
    first_state = GameState(3, 2, 3, field=field)
    assert first_state.last_move_result == "nothing"

    new_state = first_state.make_move(0, 1, "d")
    new_state.last_move_result == "draw"

    with pytest.raises(ValueError) as excinfo:
        new_state.make_move(0, 1, "g")
    assert str(excinfo.value) == "The value in the cell (0, 1) is already " \
        "set"

def test_make_move_results_no_win_or_draw():
    field = [["a", None], ["b", "e"], [None, "f"]]
    first_state = GameState(3, 2, 3, field=field)
    assert first_state.last_move_result == "nothing"

    new_state = first_state.make_move(0, 1, "c")
    assert new_state.last_move_result == "nothing"

def test_make_move_results_win():
    field = [["a", "b"], ["a", "b"], [None, "a"]]
    first_state = GameState(3, 2, 3, field=field)
    assert first_state.last_move_result == "nothing"

    new_state = first_state.make_move(2, 0, "a")
    assert new_state.last_move_result == "a"
