(function() {

  $(function() {
    if (! "WebSocket" in window) {
      $("body").text("Sorry, your browser doesn't support Web Sockets");
      return;
    }
    new Router();
    Backbone.history.start();
  });

  var Router = Backbone.Router.extend({
    routes: {
      "": "root",
      "game/:game_id": "game",
      "*notFound": "notFound"
    },

    root: function() {
      var selectGameParamsView = new SelectNewGameParamsView();
      $("body").html(selectGameParamsView.el);

      selectGameParamsView.on('newgame', function(gameParams) {
        selectGameParamsView.remove();

        var gameView = new GameView({gameParams: gameParams});
        gameView.on('exit', function() {
          gameView.remove();
          // Force triggering of "root" route.
          Backbone.history.loadUrl(Backbone.history.fragment);
        });

        $("body").html(gameView.el);
      });
    },

    game: function(gameId) {
      var gameView = new GameView({gameId: gameId});
      $("body").html(gameView.el);

      gameView.on('exit', function() {
        gameView.remove();
        this.navigate("", {trigger: true});
      }, this);
    },

    notFound: function() {
      this.navigate("", {trigger: true});
    }
  });

  var SelectNewGameParamsView = Backbone.View.extend({
    tagName: "div",

    initialize: function() {
      this._appendedViews = [];

      var MIN_FIELD_SIZE = 3,
          MAX_FIELD_SIZE = 5;

      var widthSel = new NumRangeSelectView({
        min: MIN_FIELD_SIZE,
        max: MAX_FIELD_SIZE,
        selectedVal: MIN_FIELD_SIZE
      });

      var heightSel = new NumRangeSelectView({
        min: MIN_FIELD_SIZE,
        max: MAX_FIELD_SIZE,
        selectedVal: MIN_FIELD_SIZE
      });

      var qtyToWinSel = new NumRangeSelectView({
        min: MIN_FIELD_SIZE,
        max: MIN_FIELD_SIZE,
        selectedVal: MIN_FIELD_SIZE
      });

      var gameModeSel = new RadioSelectView({items: [
          {label: "You Vs AI"    , value: "vs_ai"},
          {label: "You Vs Friend", value: "vs_hum"},
          {label: "AI Vs AI"     , value: "ai_vs_ai"}
        ]}),

        playerSignSelect = new RadioSelectView({items: [
          {label: "X", value: "x"},
          {label: "O", value: "o"}
        ]}),

        startPlayerSelect = new RadioSelectView({items: [
          {label: "You"     , value: "host"},
          {label: "Opponent", value: "opponent"}
        ]});

      var btnView = new ButtonView({title: "new game"});

      this._appendText("Create a new game");

      this._appendView(widthSel, {label: "Field Width: "});
      this._appendView(heightSel, {label: "Field Height: "});
      this._appendView(qtyToWinSel, {label: "Quantity in a row to win: "});

      this._appendView(gameModeSel, {label: "Game mode: "});
      this._appendView(playerSignSelect, {label: "Your sign: "});
      this._appendView(startPlayerSelect, {label: "Who first:"});

      this._appendView(btnView);

      function setMaxQtyToWin() {
        var whMax = Math.min(widthSel.getValue(), heightSel.getValue());
        qtyToWinSel.setRange(MIN_FIELD_SIZE, whMax);
      }
      widthSel.on("selected", setMaxQtyToWin);
      heightSel.on("selected", setMaxQtyToWin);

      gameModeSel.on("selected", function(mode) {
        var dependentViews = [playerSignSelect, startPlayerSelect];
        if (mode === "ai_vs_ai") {
          _.invoke(dependentViews, "disable");
        } else {
          _.invoke(dependentViews, "enable");
        }
      });

      btnView.on("clicked", function() {
        this.trigger("newgame", {
          field_width        : widthSel.getValue(),
          field_height       : heightSel.getValue(),
          qty_to_win         : qtyToWinSel.getValue(),
          game_type          : gameModeSel.getValue(),
          host_char          : playerSignSelect.getValue(),
          start_player_handle: startPlayerSelect.getValue(),
        });
      }, this);
    },

    _appendText: function(text) {
      this.$el.append("<p>" + text + "</p>");
     },

    _appendView: function(viewInstance, options) {
      options = options || {};
      this._appendedViews.push(viewInstance);

      if (_.isString(options.label)) {
        this.$el.append("<label>" + options.label + "</label>");
      }
      this.$el.append(viewInstance.el);
      this.$el.append("<br>");
    },

    remove: function() {
      _.invoke(this._appendedViews, "remove");
      Backbone.View.prototype.remove.call(this);
    }
  });

  var NumRangeSelectView = Backbone.View.extend({
    tagName: "select",

    events: {
      "change": "_valueChanged"
    },

    initialize: function(options) {
      if (!_.isNumber(options.min)) {
        throw new Error("min option should be provided");
      }

      if (!_.isNumber(options.max)) {
        throw new Error("max option should be provided");
      }

      if (!_.isNumber(options.selectedVal)) {
        throw new Error("selectedVal option should be provided");
      }

      this._renderOptions(options.min, options.max);
      this.setValue(options.selectedVal);
    },

    _renderOptions: function(min, max) {
      var i,
        template = _.template(
            "<option value=\"<%= value %>\"><%= text %></option>");
        html = "";

      for (i = min; i <= max; i++)
        html += template({value: i, text: i});

      this.$el.html(html);
    },

    setRange: function(min, max) {
      if (min > max) {
        throw new Error("min can't be greater that max, min=" + min + ", max=" + max);
      }

      var currentVal = this.getValue();
      this._renderOptions(min, max);
      if (currentVal > max) currentVal = max;
      if (currentVal < min) currentVal = min;
      this.setValue(currentVal);
    },

    getValue: function() {
      return parseInt(this.$el.val());
    },

    setValue: function(val) {
      this.$el.val(val);
    },

    _valueChanged: function(e) {
      this.trigger("selected", this.getValue());
    }
  });

  var RadioSelectView = Backbone.View.extend({
    tagName: "div",

    events: {
      "change input": "_valueChanged"
    },

    initialize: function(options) {
      var i,
        item,
        template = _.template(
          "<input type='radio' name='<%= name %>' value='<%= value %>'><%= label %></input>");
        html = "";

      if (!RadioSelectView.hasOwnProperty("_instances_made_")) {
        RadioSelectView._instances_made_ = 0;
      }
      var uniqInputName = "RadioSelectView" + RadioSelectView._instances_made_;
      RadioSelectView._instances_made_++;

      for (i = 0; i < options.items.length; i++) {
        item = options.items[i];
        html += template({name: uniqInputName, value: item.value, label: item.label});
      }
      this.$el.html(html).find("input:first").attr("checked", "checked");
    },

    getValue: function() {
      return this.$el.find("input:checked").val();
    },

    _valueChanged: function() {
      this.trigger("selected", this.getValue());
    },

    enable: function() {
      this.$("input").removeAttr("disabled");
    },

    disable: function() {
      this.$("input").attr("disabled", "disabled");
    }
  });

  var ButtonView = Backbone.View.extend({
    tagName: "button",

    events: {
      "click": "_clicked"
    },

    initialize: function(options) {
      this.$el.text(options.title);
    },

    _clicked: function(e) {
      e.preventDefault();
      this.trigger("clicked");
    }
  });

  var GameView = Backbone.View.extend({
    tagName: "div",

    initialize: function(options) {
      this._gameHeaderNavView = new GameHeaderNavView();
      this._gameControlsView = new GameControlsView(options);
      this.$el.append(this._gameHeaderNavView.el);
      this.$el.append(this._gameControlsView.el);

      this._gameHeaderNavView.on('exit', function() {
        this.trigger('exit');
      }, this);
    },

    remove: function() {
      this._gameHeaderNavView.remove();
      this._gameControlsView.remove();
      Backbone.View.prototype.remove.call(this);
    }
  });

  var GameHeaderNavView = Backbone.View.extend({
    tagName: "div",

    events: {
      "click button": "_exitClicked"
    },

    initialize: function() {
      this.$el.html("<button>exit game</button>");
    },

    _exitClicked: function(e) {
      e.preventDefault();
      this.trigger('exit');
    }
  });

  var GameControlsView = Backbone.View.extend({
    tagName: "div",

    initialize: function(options) {

      this._gameIsOver = false;

      if (options.hasOwnProperty("gameId")) {
        var params = {game_id: options.gameId};
      } else if (options.hasOwnProperty("gameParams")) {
        var params = options.gameParams;
      } else {
        throw new Error("gameParams or gameId should be provided.");
      };

      var wsConnectionUrl = "ws://" + location.host + "/ws?" + $.param(params);
      this._socket = new WebSocket(wsConnectionUrl);

      this._infoLogView = new InfoLogView();
      this.$el.append(this._infoLogView.el);

      this._infoLogView.log("Connecting to the server.");

      this._socket.onmessage = _.bind(function(e) {
        var msg = JSON.parse(e.data),
          data = msg.data;

        switch (msg.event) {
          case "setup":

            this._gameFieldView = new GameFieldView(data);
            this.$el.prepend(this._gameFieldView.el);

            this._gameFieldView.on("movemade", function(x, y) {
              this._socket.send(JSON.stringify({
                event: "move",
                data: {x: x, y: y}
              }));
            }, this);

            this._infoLogView.log("Connection established.");
            if (data.connection_game_id) {
              var template = _.template(
                "Send this url to your friend <%= url %>");
              var url = location.origin + "/#game/" + data.connection_game_id;
              this._infoLogView.log(template({url: url}));
            }

            if (!this._gameFieldView.isLocked()) {
              this._infoLogView.log("You first, make move.");
            }

            break;

          case "move":
            if (!this._gameFieldView) {
              throw new Error("\"setup\" event should be received first.");
            }

            this._gameFieldView.movePerformed(data.x, data.y, data.player_handle);

            // last move "move" event can arrive after the game is over.
            // Let's not unlock is this case.
            if (!this._gameIsOver) {
              this._gameFieldView.unlock();
            }

            break;

          case "playerjoined":
            if (data.player_handle === "opponent") {
              this._infoLogView.log("Your oppenent joined the game.");
            } else {
              this._infoLogView.log("One spectator joined the game.");
            }
            break;

          case "playerleft":
            if (!this._gameFieldView) {
              throw new Error("\"setup\" event should be received first.");
            }

            if (data.player_handle === "host") {
              this._gameFieldView.lock();
              this._infoLogView.log("The host left the game. Join or create a new game.");
              this._socket.close();

            } else if (data.player_handle === "opponent") {
              this._infoLogView.log("Your oppenent left the game.");
            } else {
              this._infoLogView.log("One spectator left the game.");
            }

            break;

          case "gameover":
            if (!this._gameFieldView) {
              throw new Error("\"setup\" event should be received first.");
            }

            this._gameIsOver = true;

            if (data.result_of_move === this._gameFieldView.getPlayerHandle()) {
              this._infoLogView.log("You won! Congratulations!", {color: "red"});
            } else if (data.result_of_move === "draw") {
              this._infoLogView.log("Nobody won. This is a draw.", {color: "red"});
            } else {
              this._infoLogView.log("You lost.", {color: "red"});
            }
            this._gameFieldView.lock();
            break;

          default:
            throw Error("unknown event: " + String(msg.event));
        }
      }, this);
    },

    remove: function() {
      this._socket.close();
      this._infoLogView.remove();
      this._gameFieldView.remove();
      Backbone.View.prototype.remove.call(this);
    }
  });

  var InfoLogView = Backbone.View.extend({
    tagName: "ul",

    initialize: function() {
    },

    log: function(msg, options) {
      options = _.defaults(options || {}, {color: "black"});
      var template = _.template("<li style='color: <%= color %>;'><%= msg %></li>");
      this.$el.append(template({msg: msg, color: options.color}));
    }
  });

  var GameFieldView = Backbone.View.extend({
    tagName: "div",
    className: "game-field",

    events: {
      "click .cell": "_cellClicked"
    },

    initialize: function(options) {
      this._fieldWidth = options.field_width;
      this._fieldHeight = options.field_height;
      this._field = options.field;
      this._playerHandle = options.player_handle;
      this._startPlayerHandle = options.start_player_handle;
      this._signsMap = options.signs_map;

      this._isLocked = false;

      if (this._playerHandle != "host" && this._playerHandle != "opponent") {
        this.lock();
      }

      if (this._startPlayerHandle !== this._playerHandle) {
        this.lock();
      }

      this.render();
    },

    getPlayerHandle: function() {
      return this._playerHandle;
    },

    isLocked: function() {
      return this._isLocked;
    },

    lock: function() {
      this._isLocked = true;
      this.$el.addClass("locked");
    },

    unlock: function() {
      this._isLocked = false;
      this.$el.removeClass("locked");
    },

    render: function() {
      var x, y,
        handle,
        char,
        template = _.template(
            "<div class='cell' data-pos='<%= x %>,<%= y %>'><%= char %></div>");
        html = "";

      for (y = 0; y < this._fieldHeight; y++) {
        for (x = 0; x < this._fieldWidth; x++) {
          handle = this._field[x][y];
          char = handle ? this._signsMap[handle] : "";
          html += template({x: x, y: y, char: char});
        }
        html += "<div style='clear: both;'></div>";
      }
      this.$el.html(html);
    },

    _cellClicked: function(e) {
      var pos = $(e.target).data("pos").split(",");
      var x = parseInt(pos[0]);
      var y = parseInt(pos[1]);

      if (this.isLocked() || !_.isEmpty(this._field[x][y])) {
        return;
      }

      this._field[x][y] = this._playerHandle;
      this.render();
      this.lock();

      this.trigger("movemade", x, y);
    },

    movePerformed: function(x, y, playerHandle) {
      this._field[x][y] = playerHandle;
      this.render();
    }
  });

})();
