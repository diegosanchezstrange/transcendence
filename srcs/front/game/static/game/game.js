// Check the token and redirect to the login page if it's not valid
let token = Router.getJwt();

if (!token) {
  addAlertBox("You need to be logged in to play", "danger", document.body);
  setTimeout(() => {
    Router.redirect("/login");
  }, 2000);
}
let dx;
let rectangle_left;
let rectangle_right;
let dot;
let dotX;
let dotY;

async function getGames() {
  let headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json",
    Authorization: "Bearer " + token,
  };

  //Get the oponent from the URL query param
  let url = new URL(window.location.href);
  let oponent = url.searchParams.get("oponent");

  if (!oponent) {
    addAlertBox(
      "Oponent not found",
      "danger",
      document.getElementsByTagName("main")[0],
    );
    setTimeout(() => {
      Router.changePage("/home");
    }, 2000);
  }

  // Get current games from the user

  return fetch(
    GAME_SERVICE_HOST +
      new URLSearchParams({
        oponent: oponent,
      }),
    {
      method: "GET",
      headers: headers,
    },
  )
    .then((response) => {
      if (response.status === 401) {
        throw new Error(response.status);
      }
      return response.json();
    })
    .then((data) => {
      if (data["detail"].length === 0) {
        addAlertBox(
          "No games found",
          "danger",
          document.getElementsByTagName("main")[0],
        );
        setTimeout(() => {
          Router.changePage("/home");
        }, 2000);
      } else {
        console.log(data["detail"]);
      }
    })
    .catch((error) => {
      console.log(error.message);
      let errorCode = parseInt(error.message);
      if (errorCode === 401) {
        localStorage.removeItem("token");
        Router.changePage("/login");
      }
    });
}

function createGame() {
  dx = 1;
  rectangle_left = document.getElementById("rectangle-left");
  rectangle_right = document.getElementById("rectangle-right");
  dot = document.getElementById("dot");
  dotX = 0;
  dotY = 0;

  let gameSocket = new WebSocket(
    GAME_SOCKETS_HOST + "/ws/game" + "" + "/?token=" + token,
  );

  gameSocket.onmessage = function (e) {
    const data = JSON.parse(e.data)["game_dict"];
    parse_state(data);
  };

  gameSocket.onopen = function (e) {
    console.log("connection");
  };

  gameSocket.onclose = function (e) {
    console.error("Game socket closed unexpectedly");
  };
}

function parse_state(data) {
  absolute_pos_left = data["paddle_left"];
  absolute_pos_right = data["paddle_right"];
  dotX = data["ball"][0];
  dotY = data["ball"][1];
  rectangle_left.style.top = `${absolute_pos_left}%`;
  rectangle_right.style.top = `${absolute_pos_right}%`;
  dot.style.top = `${dotY}%`;
  dot.style.left = `${dotX}%`;
}

function moveRectangleRight(dx) {
  if (
    !dotKicked ||
    rectRightPos + dx < court.offsetTop ||
    rectRightPos + dx + rectangle_right.offsetHeight >
      court.offsetTop + pongCourtHeight
  ) {
    return;
  }
  rectRightPos += dx;
  rectangle_right.style.top = `${rectRightPos}px`;
}
function moveRectangleLeft(dx) {
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

function animateDot() {
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

window.addEventListener("keydown", function (event) {
  switch (event.key) {
    case "ArrowUp":
      gameSocket.send(
        JSON.stringify({
          message: "UP",
        }),
      );
      break;
    case "ArrowDown":
      gameSocket.send(
        JSON.stringify({
          message: "DOWN",
        }),
      );
      break;
    case "Enter":
      console.log("ENTER");
      gameSocket.send(
        JSON.stringify({
          message: "ENTER",
        }),
      );
      break;
    case "w":
      gameSocket.send(
        JSON.stringify({
          message: "W",
        }),
      );
      break;
    case "s":
      gameSocket.send(
        JSON.stringify({
          message: "S",
        }),
      );
      break;
  }
});

window.addEventListener(
  "keydown",
  function (e) {
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
  },
  false,
);

async function main() {
  await getGames();
  createGame();
}

main();
