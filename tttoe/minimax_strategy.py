class MinimaxStrategy:

    def below_heuristic(self): return -1
    def above_heuristic(self): return 4
    def max_depth(self): return 5

    def heuristic(self, state):
        evaluation_map = {
            "opponent": 0,
            "nothing": 1,
            "draw": 2,
            "host": 3
        }
        return evaluation_map[state.last_move_result]

    def is_state_terminal(self, state):
        return state.last_move_result != "nothing"

    def all_substates(self, state, player):
        sign = {-1: "opponent", 1: "host"}[player]
        for x, y in state.all_available_moves():
            yield state.make_move(x, y, sign), (x, y)
