import pytest
import minimax

class Stub:
    pass

def test_check_strategy_methods_implemented():
    state = Stub()
    strategy = Stub()

    required_methods = ("below_heuristic", "above_heuristic", "max_depth", \
        "heuristic", "is_state_terminal", "all_substates")

    for method in required_methods:
        with pytest.raises(ValueError) as excinfo:
            minimax.run(state, 1, strategy)
        assert str(excinfo.value) == "strategy must implement all required " \
                "methods, \"%s\" is not implemented or not callable" % method
        setattr(strategy, method, lambda: None)

def test_check_heuristics_above_below_values_attitude():
    state = Stub()
    strategy = Stub()
    required_methods = ("max_depth", "heuristic", "is_state_terminal",
            "all_substates")
    for method in required_methods:
        setattr(strategy, method, lambda: None)

    strategy.below_heuristic = lambda: 2
    strategy.above_heuristic = lambda: 1

    with pytest.raises(ValueError) as excinfo:
        minimax.run(state, 1, strategy)
    assert str(excinfo.value) == "strategy's below_heuristic should be less " \
            "thatabove_heuristic (now below=2, above=1)"

# TODO: tests for `minimax.run` function
