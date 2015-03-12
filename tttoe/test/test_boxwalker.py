import pytest
from tttoe.boxwalker import BoxWalker

def test_init_args_validation():

    out_of_the_box_cases_args = [
            (3, 3,-1, 0),
            (3, 3, 1,-1),
            (3, 3, 3, 1),
            (3, 3, 1, 3)
    ]

    for args in out_of_the_box_cases_args:
        with pytest.raises(ValueError) as excinfo:
            BoxWalker(*args)

        assert str(excinfo.value) == "pos_x and pos_y should be inside the " \
                "box (width: %d, height: %d, x: %s, y: %s)" % args

def test_step_in_direction_args_validation():
    walker = BoxWalker(3, 3, 1, 1)

    with pytest.raises(ValueError) as excinfo:
        for pos_x, pos_y in walker.steps_in_direction(0, 0):
            pass
    assert str(excinfo.value) == "dir_x and dir_y can't be 0 at the same time"

    wrong_dir_base_msg = "dir_x and dir_y can be only -1, 0, 1, " \
            "but %d provided"

    for dir_x in [-2, 2]:
        with pytest.raises(ValueError) as excinfo:
            for pos_x, pos_y in walker.steps_in_direction(dir_x, 0):
                pass
        assert str(excinfo.value) == wrong_dir_base_msg % dir_x

    for dir_y in [-2, 2]:
        with pytest.raises(ValueError) as excinfo:
            for pos_x, pos_y in walker.steps_in_direction(0, dir_y):
                pass
        assert str(excinfo.value) == wrong_dir_base_msg % dir_y

def test_step_in_direction_without_manual_stopping():
    walker = BoxWalker(5, 5, 3, 2)

    directions_and_expectations = [
            {
                "directions": (1, 1),
                "expected_steps": [(3, 2), (4, 3), (2, 1), (1, 0)]
            }, {
                "directions": (-1, -1),
                "expected_steps": [(3, 2), (2, 1), (1, 0), (4, 3)]
            }, {
                "directions": ( 1, -1),
                "expected_steps": [(3, 2), (4, 1), (2, 3), (1, 4)]
            }, {
                "directions": (-1, 1),
                "expected_steps": [(3, 2), (2, 3), (1, 4), (4, 1)]
            }, {
                "directions": (-1, 0),
                "expected_steps": [(3, 2), (2, 2), (1, 2), (0, 2), (4, 2)]
            }, {
                "directions": (1, 0),
                "expected_steps": [(3, 2), (4, 2), (2, 2), (1, 2), (0, 2)]
            }, {
                "directions": (0, -1),
                "expected_steps": [(3, 2), (3, 1), (3, 0), (3, 3), (3, 4)]
            }, {
                "directions": (0,  1),
                "expected_steps": [(3, 2), (3, 3), (3, 4), (3, 1), (3, 0)]
            }
    ]

    for dir_and_ex in directions_and_expectations:
        steps_gen = walker.steps_in_direction(*dir_and_ex["directions"])
        steps = [(pos_x, pos_y) for pos_x, pos_y in steps_gen]
        assert steps == dir_and_ex["expected_steps"]

def test_step_in_direction_one_manual_stop():
    walker = BoxWalker(5, 5, 2, 2)
    steps = []
    for pos_x, pos_y in walker.steps_in_direction(1, 1):
        steps.append((pos_x, pos_y))
        if pos_x == 3:
            walker.turn_around_or_stop()
    assert steps == [(2, 2), (3, 3), (1, 1), (0, 0)]

def test_step_in_direction_two_manual_stops():
    walker = BoxWalker(5, 5, 2, 2)
    steps = []
    for pos_x, pos_y in walker.steps_in_direction(1, -1):
        steps.append((pos_x, pos_y))
        if pos_x == 3 or pos_x == 1:
            walker.turn_around_or_stop()
    assert steps == [(2, 2), (3, 1), (1, 3)]
