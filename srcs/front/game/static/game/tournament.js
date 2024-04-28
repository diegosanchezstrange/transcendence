class Tournament {
  constructor() {
    this.tournament_id = new URLSearchParams(window.location.search).get(
      "tournament"
    );
    this.current_game = null;
    this.winner = null;
    this.players = [];
  }

  async getPlayerStatus() {
    if (this.tournament_id === null) return;

    let headers = {
      "Content-Type": "application/json",
      Authorization: "Bearer " + Router.getJwt(),
    };

    let response = await ft_fetch(
      GAME_SERVICE_HOST +
        "/tournament/player/status/?tournament_id=" +
        this.tournament_id,
      {
        method: "GET",
        headers: headers,
      }
    );

    if (response.status !== 200) return;
    let data = await response.json();

    return data["status"];
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

    let response = await ft_fetch(GAME_SERVICE_HOST + "/tournament/nextgame/", {
      method: "POST",
      headers: headers,
      body: JSON.stringify(body),
    });
    if (response.status !== 200) return;
    let data = await response.json();

    if ("winner" in data) {
      this.winner = data["winner"];
      return this.winner;
    }
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

    let response = await ft_fetch(
      GAME_SERVICE_HOST +
        "/tournament/players/?tournament_id=" +
        this.tournament_id,
      {
        method: "GET",
        headers: headers,
      }
    );

    if (response.status !== 200) return;
    let data = await response.json();

    this.players = data["players"];
    return this.players;
  }
}

async function main_tournament() {
  let tournament = new Tournament();

  if (tournament.tournament_id === null) {
    await addAlertBox(
      "Tournament not found",
      "danger",
      document.getElementsByTagName("main")[0],
      3000
    );
    Router.changePage("/home");
    return;
  }

  if ((await tournament.getPlayerStatus()) === "ELIMINATED") {
    await addAlertBox(
      "You have been eliminated from the tournament",
      "danger",
      document.getElementsByTagName("main")[0],
      3000
    );
    Router.changePage("/home");
    return;
  }

  await tournament.getCurrentGame();

  if (tournament.current_game !== null) {
    if (tournament.current_game.playerLeftId === Router.getUserId()) {
      Router.changePage(
        "/pong/?opponent=" + tournament.current_game.playerRight
      );
    } else if (tournament.current_game.playerRightId === Router.getUserId()) {
      Router.changePage(
        "/pong/?opponent=" + tournament.current_game.playerLeft
      );
    }
  } else if (tournament.winner !== null) {
    await addAlertBox(
      tournament.winner + " has won the game",
      "success",
      document.getElementsByTagName("main")[0],
      3000
    );
    Router.changePage("/home");
    return;
  } else {
    await addAlertBox(
      "Game not found",
      "danger",
      document.getElementsByTagName("main")[0],
      3000
    );
    Router.changePage("/home");
    return;
  }
}

main_tournament();

window.addEventListener("change-page", function (event) {
  if (event.detail.newPage.includes("/tournament")) {
    main_tournament();
  }
});
