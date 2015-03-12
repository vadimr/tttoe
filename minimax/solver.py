# pylint: disable=super-init-not-called
"""
This module implements the Minimax method (http://en.wikipedia.org/wiki/Minimax)
It can be used for implementing AI for a variety of two-player zero-sum games,
such as chess, checkers, tic-tac-toe etc.

This implementation implements Alpha–beta pruning
http://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning

See `run` method docs.
"""

from minimax.keeper_of_min_or_max import KeeperOfMinOrMax

class NoSubstatesReturned(Exception):
    """Exception raised if no substates returned from the specific game_state.
    Possible cause: terminal state reached, but stategy's "is_state_terminal"
    method didn't indicate it (wrong strategy implementation).

    Attributes:
        game_state
        strategy
    """
    def __init__(self, game_state, strategy):
        self.game_state = game_state
        self.strategy = strategy

def _max(game_state, strategy, alpha, beta, depth):

    if strategy.is_state_terminal(game_state) or depth > strategy.max_depth():
        value = strategy.heuristic(game_state)
        return (value, None)

    max_keeper = KeeperOfMinOrMax.max()

    for new_game_state, payload in strategy.all_substates(game_state, 1):
        value, _ = _min(new_game_state, strategy, alpha, beta, depth + 1)
        if value >= beta:
            return value, payload
        max_keeper.check_keep_or_reject(value, payload=payload)
        alpha = max_keeper.value()

    if max_keeper.value() == None:
        raise NoSubstatesReturned(game_state, strategy)

    return max_keeper.value(), max_keeper.payload()

def _min(game_state, strategy, alpha, beta, depth):

    if strategy.is_state_terminal(game_state) or depth > strategy.max_depth():
        value = strategy.heuristic(game_state)
        return (value, None)

    min_keeper = KeeperOfMinOrMax.min()

    for new_game_state, payload in strategy.all_substates(game_state, -1):
        value, _ = _max(new_game_state, strategy, alpha, beta, depth + 1)
        if value <= alpha:
            return value, payload
        min_keeper.check_keep_or_reject(value, payload=payload)
        beta = min_keeper.value()

    if min_keeper.value() == None:
        raise NoSubstatesReturned(game_state, strategy)

    return min_keeper.value(), min_keeper.payload()

def run(game_state, player, strategy):
    """Runs the Minimax algorithm. Returns the payload for the optimal possible
    state if this state exists, or None (it means that the passed game_state is
    terminal.

    Arguments:

        game_state -- any object which will be passed to the strategy
        player - number -1 or 1. Indicates "min" or "max" player.
        strategy - object which implements the required methods (see below).

    The strategy object should implement thsese methods:

    max_depth -- should return the allowed recursion depth. The higher the
        value the smarter AI (and worse performance). Should be chosen for a
        specific task.

    heuristic(game_state) -- accepts the game_state object. Should return
        comparable number. Usually the value should be greater if the 1 player
        closer to victory, and smaller if the -1 player closer to victory.

    below_heuristic -- should return a number, which is less than any number
        returned by `heuristic` method (for Alpha-beta pruning).

    above_heuristic -- should return a number, which is greater than any number
        returned by `heuristic` method (for Alpha-beta pruning).

    is_state_terminal(game_state) -- accepts the game_state, returns True
        if the state is terminal (some player won or we have a draw)

    all_substates(game_state, player) -- should return a generator which
        generates all possible states, which can be made by the player from the
        original game_state (usually it means that we need to get all possible
        game moves from the state).
        In this method you need to yield new state and the payload. The payload
        will be returned by the `run` method at the end of execution (or None
        if the optimal state can't be found).

    Strategy implementation example:

    class TicTacToeSimpleStrategy:

        def below_heuristic(self): return -1
        def above_heuristic(self): return 4
        def max_depth(self): return 3

        def heuristic(self, state):
            evaluation_map = {
                "o": 0,
                "nothing": 1,
                "draw": 2,
                "x": 3
            }
            return evaluation_map[state.last_step_result()]

        def is_state_terminal(self, state):
            return state.last_step_result() != GameState.NOTHING

        def all_substates(self, state, player):
            sign = {-1: "o", 1: "x"}[player]
            for x, y in state.all_available_steps():
                # Here we pass (x,y) as a payload
                yield state.make_move(x, y, sign), (x, y)

    game_state = GameState(3, 3, 3)

    minimax.run(game_state, 1, TicTacToeSimpleStrategy())
    # Returns (x,y) of the optimal possible move, which can be made by AI
    # or None if the game_state is terminal (the winner already exist, or it's
    # a draw.
    """

    all_strategy_attribs = dir(strategy)
    for required_method in ("below_heuristic", "above_heuristic", "max_depth", \
            "heuristic", "is_state_terminal", "all_substates"):
        if (required_method not in all_strategy_attribs) or \
            (not callable(getattr(strategy, required_method))):
            raise ValueError("strategy must implement all required " \
                    "methods, \"%s\" is not implemented or not callable" % \
                        required_method)

    if strategy.below_heuristic() >= strategy.above_heuristic():
        raise ValueError("strategy's below_heuristic should be less that" \
                "above_heuristic (now below=%d, above=%d)" % \
                (strategy.below_heuristic(), strategy.above_heuristic()))

    player2func = {-1: _min, 1: _max}
    if player not in player2func.keys():
        raise ValueError("Player can be only: %s" % ", ".join(player2func.keys()))

    func = player2func[player]
    _, payload = func(game_state, strategy, \
            strategy.below_heuristic(), strategy.above_heuristic(), 0)
    return payload
