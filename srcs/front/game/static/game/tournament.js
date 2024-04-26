class Tournament {
  constructor() {
    this.tournament_id = new URLSearchParams(window.location.search).get(
      "tournament",
    );
    this.current_game = null;
    this.players = [];
  }

  async getCurrentGame() {
    if (this.tournament_id === null) return;
    if (this.current_game !== null) return this.current_game;

    let headers = {
      "Content-Type": "application/json",
      Authorization: "Bearer " + Router.getJwt(),
    };

    let body = {
      tournament_id: this.tournament_id,
    };

    let response = await fetch(GAME_SERVICE_HOST + "/tournament/nextgame/", {
      method: "POST",
      headers: headers,
      body: JSON.stringify(body),
    });
    if (response.status !== 200) return;
    let data = await response.json();

    this.current_game = data["game"];
    return this.current_game;
  }

  async getPlayers() {
    if (this.tournament_id === null) return;
    if (this.players.length > 0) return this.players;

    let headers = {
      "Content-Type": "application/json",
      Authorization: "Bearer " + Router.getJwt(),
    };

    let response = await fetch(
      GAME_SERVICE_HOST +
        "/tournament/players/?tournament_id=" +
        this.tournament_id,
      {
        method: "GET",
        headers: headers,
      },
    );

    if (response.status !== 200) return;
    let data = await response.json();

    this.players = data["players"];
    return this.players;
  }
}

function main() {
  let tournament = new Tournament();

  tournament.getCurrentGame();

  if (tournament.current_game.playerLeft === Router.getUsername()) {
    document.getElementById("player-left").innerText = "You";
    Router.changePage("/pong/?opponent=" + tournament.current_game.playerRight);
  } else if (tournament.current_game.playerRight === Router.getUsername()) {
    document.getElementById("player-right").innerText = "You";
    Router.changePage("/pong/?opponent=" + tournament.current_game.playerLeft);
  } else {
    document.getElementById("player-left").innerText =
      tournament.current_game.playerLeft;
    document.getElementById("player-right").innerText =
      tournament.current_game.playerRight;
  }
}

main();
