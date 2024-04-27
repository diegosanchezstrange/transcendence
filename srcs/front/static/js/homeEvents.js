function extractOpponentFromResponse(response) {
  let opponent;
  if (response.playerLeft === Router.getUsername()) {
    opponent = response.playerRight;
  } else {
    opponent = response.playerLeft;
  }
  return opponent;
}

async function find1v1Game() {
  // Find any games on waiting status or paused status
  //

  if (Router.getJwt() === null) {
    Router.changePage("/login");
    return;
  }

  let headers = {
    "Content-Type": "application/json",
    Authorization: "Bearer " + Router.getJwt(),
  };

  id = Router.getUserId();
  let url = GAME_SERVICE_HOST + "/game/" + id;
  let games = await fetch(url + "/?status=WAITING", {
    method: "GET",
    headers: headers,
  });

  let games_detail = (await games.json())["detail"];

  let pause_games = await fetch(url + "/?status=PAUSED", {
    method: "GET",
    headers: headers,
  });

  let pause_games_detail = (await pause_games.json())["detail"];

  if (pause_games.status === 200 && pause_games_detail.length > 0) {
    let game = pause_games_detail;
    if (game.length == 1) {
      let opponent = extractOpponentFromResponse(game[0]);
      await addAlertBox(
        "Game paused found with " + opponent,
        "success",
        document.getElementsByTagName("main")[0],
        2000
      );
      Router.changePage("/pong/?opponent=" + opponent);
    } else if (game.length > 1) {
      await addAlertBox(
        "Error: more than one game found",
        "danger",
        document.getElementsByTagName("main")[0],
        3000
      );
    }
  } else if (games.status === 200 && games_detail.length > 0) {
    let game = games_detail;
    if (game.length == 1) {
      let opponent = extractOpponentFromResponse(game[0]);
      await addAlertBox(
        "Game found with " + opponent,
        "success",
        document.getElementsByTagName("main")[0],
        2000
      );
      Router.changePage("/pong/?opponent=" + opponent);
    } else if (game.length > 1) {
      await addAlertBox(
        "Error: more than one game found",
        "danger",
        document.getElementsByTagName("main")[0],
        3000
      );
    }
  } else {
    let alert = await addAlertBox(
      "Joining queue...",
      "success",
      document.getElementsByTagName("main")[0]
    );
    response = await fetch(MATCHMAKING_SERVICE_HOST + "/queue/join/", {
      method: "POST",
      headers: headers,
    });
    if (response.status != 200) {
      alert.remove();
      await addAlertBox(
        "Error joining queue",
        "danger",
        document.getElementsByTagName("main")[0],
        3000
      );
    }
  }
}

async function enterLobby() {
  // Find any tournaments on waiting status or paused status
  //

  if (Router.getJwt() === null) {
    Router.changePage("/login");
    return;
  }

  let headers = {
    "Content-Type": "application/json",
    Authorization: "Bearer " + Router.getJwt(),
  };

  let tournament = await fetch(GAME_SERVICE_HOST + "/tournament/", {
    method: "GET",
    headers: headers,
  });

  if (tournament.status === 200) {
    let tournament_detail = (await tournament.json())["detail"];
    for (let i = 0; i < tournament_detail.length; i++) {
      if (
        tournament_detail[i].status === "WAITING" ||
        tournament_detail[i].status === "IN_PROGRESS"
      ) {
        let tournament_id = tournament_detail[i].id;
        Router.changePage("/lobby/?tournament=" + tournament_id);
        return;
      }
    }
  }
  // no tournament found
  let new_tournament = await fetch(
    MATCHMAKING_SERVICE_HOST + "/tournament/join/",
    {
      method: "POST",
      headers: headers,
    }
  );

  if (new_tournament.status === 200) {
    await addAlertBox(
      "Waiting for other players...",
      "success",
      document.getElementsByTagName("main")[0]
    );
  }
}
