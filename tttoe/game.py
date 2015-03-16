import uuid
from tttoe.gamestate import GameState

class Game:
    def __init__(self, field_width, field_height, qty_to_win, \
            start_player_handle, host_char):

        self._start_player_handle = start_player_handle
        self._host_char = host_char
        self._spectators_count = 0

        self._players_hash = dict()
        self._game_id = uuid.uuid4().hex
        self._is_over = False

        self.game_state = GameState(field_width, field_height, qty_to_win)

    @property
    def start_player_handle(self):
        return self._start_player_handle

    @property
    def host_char(self):
        return self._host_char

    @property
    def game_id(self):
        return self._game_id

    @property
    def is_over(self):
        return self._is_over

    def perform_move(self, player_handle, x, y):
        if player_handle not in ["host", "opponent"]:
            raise ValueError("Only host or opponent can make moves, not \"%s\"" \
                % player_handle)

        self.game_state = self.game_state.make_move(x, y, player_handle)

        res = self.game_state.last_move_result
        if res != "nothing":
            self._is_over = True
            data = dict(event="gameover", data=dict(result_of_move=res))
            for player in self._players_hash.values():
                player.write_message(data)

        for handle, player in self._players_hash.items():
            data = dict(event="move", data=dict(player_handle=player_handle, \
                x=x, y=y))
            if handle != player_handle:
                player.write_message(data)

    def player_left(self, player_handle):
        del self._players_hash[player_handle]
        data = dict(event="playerleft", data=dict(player_handle=player_handle))
        for player in self._players_hash.values():
            player.write_message(data)

    def append_player(self, socket_or_ai):
        if "host" not in self._players_hash:
            player_handle = "host"
        elif "opponent" not in self._players_hash:
            player_handle = "opponent"
        else:
            player_handle = "spectator_%d" % self._spectators_count
            self._spectators_count += 1

        self._players_hash[player_handle] = socket_or_ai

        for handle, player in self._players_hash.items():
            data = dict(event="playerjoined", data=dict(player_handle=player_handle))
            if handle != player_handle:
                player.write_message(data)

        return player_handle
