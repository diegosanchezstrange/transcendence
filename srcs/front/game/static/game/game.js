let game = null;

class Game {
  constructor() {
    this.dx = 1;
    this.rectangle_left = document.getElementById("rectangle-left");
    this.rectangle_right = document.getElementById("rectangle-right");
    this.dot = document.getElementById("dot");
    this.dotX = 0;
    this.dotY = 0;
    this.gameSocket = null;
  }
  async getGames() {
    let token = Router.getJwt();
    let headers = {
      "X-Requested-With": "XMLHttpRequest",
      "Content-Type": "application/json",
      Authorization: "Bearer " + token,
    };

    //Get the oponent from the URL query param
    let oponent = new URLSearchParams(window.location.search).get("opponent");

    if (!oponent) {
      await addAlertBox(
        "Oponent not found",
        "danger",
        document.getElementsByTagName("main")[0],
        3000
      );
      Router.changePage("/home");
      return;
    }

    let invitations = await fetch(
      GAME_SERVICE_HOST + "/challenge/?opponent=" + oponent + "&status=PENDING",
      {
        method: "GET",
        headers: headers,
      }
    );

    let games = await fetch(
      GAME_SERVICE_HOST + "/game/?opponent=" + oponent + "&status=WAITING",
      {
        method: "GET",
        headers: headers,
      }
    );

    let pause_games = await fetch(
      GAME_SERVICE_HOST + "/game/?opponent=" + oponent + "&status=PAUSED",
      {
        method: "GET",
        headers: headers,
      }
    );

    if (pause_games.status === 200) {
      let game = await pause_games.json();
      if (game["detail"].length > 0)
        return { game: game["detail"][0], type: "game" };
    }

    if (games.status === 200) {
      let game = await games.json();
      if (game["detail"].length > 0)
        return { game: game["detail"][0], type: "game" };
    }

    if (invitations.status === 200) {
      let invitation = await invitations.json();
      if (invitation["detail"].length > 0)
        return { game: invitation["detail"][0], type: "invitation" };
    }

    return null;
  }
  async createGame(game) {
    if (game == null) {
      await addAlertBox("Game not found", "danger", document.body, 3000);
      Router.changePage("/home/");
      return;
    }

    let gameType = game.type;
    let gameData = game.game;

    let socket_params;

    if (gameType === "game") {
      let game_id = gameData.id;
      socket_params = "&game=" + game_id;
    } else if (gameType === "invitation") {
      let challenge_id = gameData.id;
      socket_params = "&invitation=" + challenge_id;
    }

    // dx = 1;
    // rectangle_left = document.getElementById("rectangle-left");
    // rectangle_right = document.getElementById("rectangle-right");
    // dot = document.getElementById("dot");
    // dotX = 0;
    // dotY = 0;

    let token = Router.getJwt();

    console.log("Connecting to game socket");

    this.gameSocket = new WebSocket(
      GAME_SOCKETS_HOST + "/game" + "/?token=" + token + socket_params
    );

    this.gameSocket.onmessage = async (e) => {
      const data = JSON.parse(e.data);

      if (data.hasOwnProperty("game_dict")) {
        this.parse_state(data["game_dict"]);
      } else if (data.hasOwnProperty("score_dict")) {
        this.changeScore(data["score_dict"]);
      } else if (data.hasOwnProperty("end_dict")) {
        let endData = data["end_dict"];

        if (endData.hasOwnProperty("error")) {
          let message = endData["error"];
          await addAlertBox(message, "danger", document.body, 4000);
          Router.changePage("/home/");
        } else {
          let winner = endData["winner"];
          let message = winner + " won the game";
          await addAlertBox(message, "success", document.body, 4000);
          if (endData.hasOwnProperty("tournament_id"))
            Router.changePage("/lobby/?tournament=" + endData["tournament_id"]);
          else Router.changePage("/home/");
        }
      }
    };

    this.gameSocket.onopen = function (e) {
      console.log("connection");
    };

    this.gameSocket.onclose = function (e) {
      console.log("connection closed");
    };
  }

  parse_state(data) {
    let absolute_pos_left = data["paddle_left"];
    let absolute_pos_right = data["paddle_right"];
    this.dotX = data["ball"][0];
    this.dotY = data["ball"][1];
    this.rectangle_left.style.top = `${absolute_pos_left}%`;
    this.rectangle_right.style.top = `${absolute_pos_right}%`;
    this.dot.style.top = `${this.dotY}%`;
    this.dot.style.left = `${this.dotX}%`;
  }

  changeScore(score) {
    let score_left = score["left"];
    let score_right = score["right"];

    let score_left_element = document.getElementById("scoreLeft");
    let score_right_element = document.getElementById("scoreRight");

    score_left_element.innerHTML = score_left;
    score_right_element.innerHTML = score_right;
  }

  moveRectangleRight(dx) {
    if (
      !this.dotKicked ||
      this.rectRightPos + dx < this.court.offsetTop ||
      this.rectRightPos + dx + this.rectangle_right.offsetHeight >
        this.court.offsetTop + pongCourtHeight
    ) {
      return;
    }
    rectRightPos += dx;
    rectangle_right.style.top = `${rectRightPos}px`;
  }
  moveRectangleLeft(dx) {
    if (
      !dotKicked ||
      rectLeftPos + dx < court.offsetTop ||
      rectLeftPos + dx + rectangle_left.offsetHeight >
        court.offsetTop + pongCourtHeight
    ) {
      return;
    }
    rectLeftPos += dx;
    rectangle_left.style.top = `${rectLeftPos}px`;
  }

  animateDot() {
    if (!dotKicked) {
      return;
    }
    let rectRightBounds = rectangle_right.getBoundingClientRect();
    let rectLeftBounds = rectangle_left.getBoundingClientRect();
    if (dotSpeedX > 0 && dotX + dotSpeedX > rectRightBounds.left) {
      dotX += dotX + dotSpeedX - rectRightBounds.left;
    } else {
      dotX += dotSpeedX;
    }
    dotY += dotSpeedY;
    dot.style.left = `${dotX}px`;
    dot.style.top = `${dotY}px`;
    let courtBounds = court.getBoundingClientRect();
    let dotBounds = dot.getBoundingClientRect();

    if (
      dotBounds.right <= rectLeftBounds.left ||
      dotBounds.left >= rectRightBounds.right
    ) {
      dotKicked = false;
      start = false;
    }
    //pegarle de frente IZQ
    if (
      dotSpeedX < 0 &&
      dotBounds.left <= rectLeftBounds.right &&
      dotBounds.top >= rectLeftBounds.top &&
      dotBounds.bottom <= rectLeftBounds.bottom
    ) {
      dotSpeedY = (dotSpeedY + Math.random()) * -1;
      dotSpeedX = (dotSpeedX + Math.random()) * -1;
    }
    // pegarle por debajo IZQ
    else if (
      dotBounds.top === rectLeftBounds.bottom &&
      dotBounds.left >= rectLeftBounds.left &&
      dotBounds.left <= rectLeftBounds.right
    ) {
      dotSpeedY = (dotSpeedY + Math.random()) * -1;
      dotSpeedX = (dotSpeedX + Math.random()) * -1;
    }
    //pegarle de frente DER
    else if (
      dotSpeedX > 0 &&
      dotBounds.right >= rectRightBounds.left &&
      dotBounds.top >= rectRightBounds.top &&
      dotBounds.bottom <= rectRightBounds.bottom
    ) {
      dotSpeedY = (dotSpeedY + Math.random()) * -1;
      dotSpeedX = (dotSpeedX + Math.random()) * -1;
    }
    // pegarle por debajop DER
    else if (
      dotBounds.top === rectRightBounds.bottom &&
      dotBounds.right >= rectLeftBounds.left &&
      dotBounds.right <= rectLeftBounds.right
    ) {
      dotSpeedY = (dotSpeedY + Math.random()) * -1;
      dotSpeedX = (dotSpeedX + Math.random()) * -1;
    }
    // Rebotar contra las paredes de arriba o abajo
    else if (
      (dotSpeedY < 0 && dotBounds.top <= court.offsetTop) ||
      (dotBounds.bottom >= courtBounds.bottom && dotSpeedY > 0)
    ) {
      dotSpeedY = (dotSpeedY + Math.random()) * -1;
    }
    // salirse del court
    else if (
      dotBounds.left <= courtBounds.left ||
      dotBounds.left + dot.offsetWidth >= courtBounds.right
    ) {
      dotKicked = false;
      start = false;
    }
    if (dotKicked) {
      requestAnimationFrame(animateDot);
    }
  }
}

function handleKeyDownArrows(event, game) {
  switch (event.key) {
    case "ArrowUp":
      game.gameSocket.send(
        JSON.stringify({
          message: "UP",
        })
      );
      break;
    case "ArrowDown":
      game.gameSocket.send(
        JSON.stringify({
          message: "DOWN",
        })
      );
      break;
    case "Enter":
      console.log("ENTER");
      game.gameSocket.send(
        JSON.stringify({
          message: "ENTER",
        })
      );
      break;
    case "w":
      game.gameSocket.send(
        JSON.stringify({
          message: "W",
        })
      );
      break;
    case "s":
      game.gameSocket.send(
        JSON.stringify({
          message: "S",
        })
      );
      break;
  }
}

function handleKeysPreventDefault(e) {
  if (
    [
      "ArrowUp",
      "ArrowDown",
      "ArrowLeft",
      "ArrowRight",
      "Enter",
      "A",
      "S",
    ].indexOf(e.code) > -1
  ) {
    e.preventDefault();
  }
}

async function main_game() {
  // Check the token and redirect to the login page if it's not valid
  let token = Router.getJwt();
  game = new Game();

  if (!token) {
    addAlertBox("You need to be logged in to play", "danger", document.body);
    setTimeout(() => {
      Router.changePage("/login");
    }, 2000);
  }
  let gameData = await game.getGames();
  game.createGame(gameData);

  let wrapperFunction = function (event) {
    handleKeyDownArrows(event, game);
  };

  window.removeEventListener("keydown", wrapperFunction, false);
  window.addEventListener("keydown", wrapperFunction, false);

  window.removeEventListener("keydown", handleKeysPreventDefault, false);
  window.addEventListener("keydown", handleKeysPreventDefault, false);
}

main_game();

window.addEventListener("change-page", function (event) {
  //Check if the url has /pong/
  //If it has execute the main_game function
  if (game) {
    game.gameSocket.close();
    game = null;
  }
  if (event.detail.newPage.includes("/pong/")) {
    main_game();
  }
});
