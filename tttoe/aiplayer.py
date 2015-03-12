import minimax
from tttoe.minimax_strategy import MinimaxStrategy

class AIPlayer:
    def __init__(self, game):
        self._game = game
        self._player_handle = self._game.append_player(self)

    @property
    def player_handle(self):
        return self._player_handle

    def write_message(self, msg):
        event = msg["event"]

        if event == "setup":
            pass
        elif event == "move":
            self.make_move()

        elif event == "playerleft":
            pass
        elif event == "gameover":
            pass
        elif event == "playerjoined":
            pass
        else:
            raise ValueError("Unknown event: %s" % event)

    def make_move(self):
        if self._game.is_over:
            return

        res = self._game.game_state.last_move_result
        if res != "nothing":
            raise Exception("Game terminal state already reached \"%s\"", res)

        pl = dict(host=1, opponent=-1)[self._player_handle]
        x, y = minimax.run(self._game.game_state, pl, MinimaxStrategy())
        self._game.perform_move(self._player_handle, x, y)
