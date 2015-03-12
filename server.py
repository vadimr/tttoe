import os.path
from tornado.options import define, options, parse_command_line
from tornado.web import RequestHandler, Application, url
from tornado.websocket import WebSocketHandler
from tornado.ioloop import IOLoop
from tornado.escape import json_decode

from tttoe.aiplayer import AIPlayer
from tttoe.game import Game

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")

global_games_hash = dict()

class GameWebSocket(WebSocketHandler):
    def open(self):
        self._connection_game_id = None

        game_id = self.get_argument("game_id", None)
        if game_id:
            self._game = global_games_hash[game_id]
            self._setup_current_player()

        else:
            field_width         = int(self.get_argument("field_width"))
            field_height        = int(self.get_argument("field_height"))
            qty_to_win          = int(self.get_argument("qty_to_win"))
            host_char           =     self.get_argument("host_char")
            start_player_handle =     self.get_argument("start_player_handle")
            game_type           =     self.get_argument("game_type")

            self._game = Game(field_width, field_height, qty_to_win, \
                    start_player_handle, host_char)

            if game_type == "vs_ai":
                self._setup_current_player()
                ai = AIPlayer(self._game)
                if ai.player_handle == self._game.start_player_handle:
                    ai.make_move()

            elif game_type == "vs_hum":
                global_games_hash[self._game.game_id] = self._game
                self._connection_game_id = self._game.game_id
                self._setup_current_player()

            elif game_type == "ai_vs_ai":
                ai_1 = AIPlayer(self._game)
                AIPlayer(self._game)
                self._setup_current_player()
                ai_1.make_move()

            else:
                raise ValueError("Unknow game type provided: \"%s\"" % game_type)

    def _setup_current_player(self):
        self._player_handle = self._game.append_player(self)
        data = dict(event="setup", data=dict(
            connection_game_id=self._connection_game_id,
            player_handle=self._player_handle,
            signs_map=dict(host=self._game.host_char, opponent=dict(x="o", o="x")[self._game.host_char]),
            start_player_handle=self._game.start_player_handle,
            field_width=self._game.field_width,
            field_height=self._game.field_height,
            field=self._game.game_state.field
            ))
        self.write_message(data)

    def on_message(self, message):
        msg = json_decode(message)
        event = msg["event"]
        if event == "move":
            data = msg["data"]
            self._game.perform_move(self._player_handle, data["x"], data["y"])
        else:
            raise ValueError("Unknown event: %s" % event)

    def on_close(self):
        self._game.player_left(self._player_handle)
        if self._player_handle == "host" and self._game.game_id in global_games_hash:
            del global_games_hash[self._game.game_id]

class RootHttpHandler(RequestHandler):
    def get(self):
        self.render("client.html")

def main():
    parse_command_line()
    app = Application([
            url(r"/", RootHttpHandler),
            url(r"/ws", GameWebSocket)
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=options.debug
    )
    app.listen(options.port)
    IOLoop.current().start()

if __name__ == "__main__":
    main()
