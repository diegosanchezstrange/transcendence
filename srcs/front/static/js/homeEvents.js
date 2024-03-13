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
  
  let games = await fetch(GAME_SERVICE_HOST + "/?status=WAITING", {
    method: "GET",
    headers: headers,
  });
  
  let games_detail = (await games.json())["detail"];
  
  let pause_games = await fetch(GAME_SERVICE_HOST + "/?status=PAUSED", {
    method: "GET",
    headers: headers,
  });
  
  let pause_games_detail = (await pause_games.json())["detail"];
  
  if (pause_games.status === 200 && pause_games_detail.length > 0) {
    let game = pause_games_detail;
    if (game.length == 1) {
      let opponent = extractOpponentFromResponse(game[0]);
      let alert = addAlertBox(
        "Game paused found with " + opponent,
        "success",
        document.getElementsByTagName("main")[0]
        );
        await new Promise((resolve) => setTimeout(resolve, 2000));
        alert.remove();
        Router.changePage("/pong/?opponent=" + opponent);
    }
    else if (game.length > 1) {
      let alert = addAlertBox(
        "Error: more than one game found",
        "danger",
        document.getElementsByTagName("main")[0]
        );
      await new Promise((resolve) => setTimeout(resolve, 2000));
      alert.remove();
      }
      else if (games.status === 200 && games_detail.length > 0) {
        let game = games_detail;
        if (game.length == 1) {
          let opponent = extractOpponentFromResponse(game[0]);
          let alert = addAlertBox(
            "Game found with " + opponent,
            "success",
            document.getElementsByTagName("main")[0]
          );
          await new Promise((resolve) => setTimeout(resolve, 2000));
          alert.remove();
          Router.changePage("/pong/?opponent=" + opponent);
        }
        else if (game.length > 1) {
          let alert = addAlertBox(
            "Error: more than one game found",
            "danger",
            document.getElementsByTagName("main")[0]
            );
            await new Promise((resolve) => setTimeout(resolve, 2000));
            alert.remove();
        }
        else {
          let alert = addAlertBox(
            "Joining queue...",
            "success",
            document.getElementsByTagName("main")[0]
          );
          response = await fetch(MATCHMAKING_SERVICE_HOST + "/queue/join/", {
            method: "POST",
            headers: headers,
          });
          if (response.status === 200) {
            await new Promise((resolve) => setTimeout(resolve, 2000));
            alert.remove();
          }
          else {
            alert.remove();
            alert = addAlertBox(
              "Error joining queue",
              "danger",
              document.getElementsByTagName("main")[0]
            );
            await new Promise((resolve) => setTimeout(resolve, 2000));
            alert.remove();
          }
        }
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
  
  let tournament_detail = (await tournament.json())["detail"];
  
  if (tournament_detail.length == 0) // no tournament found
  {
    let new_tournament = await fetch(GAME_SERVICE_HOST + "/tournament/", {
      method: "POST",
      headers: headers,
    });
    tournament_detail = (await new_tournament.json())["detail"];
  }
  let tournament_id = tournament_detail[0].id;
  Router.changePage("/lobby?tournament_id=" + tournament_id);
  
  let joined_tournament = await fetch(MATCHMAKING_SERVICE_HOST + "/tournament/join/", {
    method: "POST",
    headers: headers,
  });
  
  if (joined_tournament.status === 200) {
    let alert = addAlertBox(
      "Waiting for other players...",
      "success",
      document.getElementsByTagName("main")[0]
    );
  }
}
                  