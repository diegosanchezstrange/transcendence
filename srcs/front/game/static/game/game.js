dx = 1;
let rectangle_left = document.getElementById('rectangle-left');
let rectangle_right = document.getElementById('rectangle-right');
let dot = document.getElementById('dot');
const gameSocket = new WebSocket(
    'ws://'
    + 'localhost:8000'
    + '/ws/game/test/');
gameSocket.onmessage = function(e) {
    const data = JSON.parse(e.data)["game_dict"];
    // read dgame state dictionary from data to generate relative
    // positions of the game elements considering the values as percentages
    // of the court size
    // update the game elements positions
    parse_state(data);
};
gameSocket.onopen = function(e)
{
  console.log("connection")
}
function parse_state(data){
  absolute_pos_left = data['paddle_left'];
  absolute_pos_right = data['paddle_right'];
  dotX = data['ball'][0];
  dotY = data['ball'][1];
  rectangle_left.style.top = `${absolute_pos_left}%`;
  rectangle_right.style.top = `${absolute_pos_right}%`;
  //console.log(dotX);
  //console.log(dotY);
  dot.style.top = `${dotY}%`
  dot.style.left = `${dotX}%`
}
gameSocket.onclose = function(e) {
    console.error('Game socket closed unexpectedly');
}


function moveRectangleRight(dx) {

  if (!dotKicked || rectRightPos + dx < court.offsetTop || rectRightPos + dx + rectangle_right.offsetHeight > court.offsetTop + pongCourtHeight) {
    return;
  }
  rectRightPos += dx;
  rectangle_right.style.top = `${rectRightPos}px`;
}
function moveRectangleLeft(dx) {
  if (!dotKicked || rectLeftPos + dx < court.offsetTop || rectLeftPos + dx + rectangle_left.offsetHeight > court.offsetTop + pongCourtHeight) {
    return;
  }
  rectLeftPos += dx;
  rectangle_left.style.top = `${rectLeftPos}px`;
}

function kickDot() {
  if (!dotKicked && !start){
    dotX = pongCourtWidth / 2 + court.offsetLeft - dot.offsetWidth / 2;
    dotY = pongCourtHeight / 2 +court.offsetTop- dot.offsetHeight / 2;
    dot.style.left = `${dotX}px`;
    dot.style.top = `${dotY}px`;
    dotSpeedX = vel * [1, -1].sample();
    dotSpeedY = vel* [1, -1].sample();
    rectangle_right.style.top = `${top_rect}px`;
    rectangle_left.style.top = `${top_rect}px`;
    rectRightPos = top_rect;
    rectLeftPos = top_rect;
    start = true
    return;
  }
  if (!dotKicked && start) {
    dotKicked = true;
    animateDot();
  }


}

function animateDot() {

  if (!dotKicked) {
    return;
  }
  let rectRightBounds = rectangle_right.getBoundingClientRect();
  let rectLeftBounds = rectangle_left.getBoundingClientRect();
  if ( dotSpeedX > 0 &&  dotX + dotSpeedX > rectRightBounds.left)
  {
    console.log(dotSpeedX)
    dotX += dotX + dotSpeedX - rectRightBounds.left;
  }
  else
  {
    dotX += dotSpeedX;
  }
  dotY += dotSpeedY;
  dot.style.left = `${dotX}px`;
  dot.style.top = `${dotY}px`;
  let courtBounds = court.getBoundingClientRect();
  let dotBounds = dot.getBoundingClientRect();

  if (dotBounds.right <= rectLeftBounds.left || dotBounds.left >= rectRightBounds.right) {
    dotKicked = false;
    start = false;
  }
  //pegarle de frente IZQ
  if (dotSpeedX < 0 && dotBounds.left <= rectLeftBounds.right  && dotBounds.top >= rectLeftBounds.top  && dotBounds.bottom <= rectLeftBounds.bottom)
  {
    dotSpeedY = (dotSpeedY+ Math.random())*-1;
    dotSpeedX = (dotSpeedX+ Math.random())*-1;
  }
  // pegarle por debajo IZQ
  else if (dotBounds.top === rectLeftBounds.bottom && dotBounds.left >=  rectLeftBounds.left && dotBounds.left <= rectLeftBounds.right)
  {
    dotSpeedY = (dotSpeedY + Math.random()) *-1;
    dotSpeedX = (dotSpeedX + Math.random())*-1;
  }
  //pegarle de frente DER
  else if ( dotSpeedX > 0 && dotBounds.right >= rectRightBounds.left && dotBounds.top >= rectRightBounds.top && dotBounds.bottom <= rectRightBounds.bottom)
  {
    dotSpeedY = (dotSpeedY + Math.random()) *-1;
    dotSpeedX = (dotSpeedX + Math.random())*-1;
  }
  // pegarle por debajop DER
  else if (dotBounds.top === rectRightBounds.bottom && dotBounds.right >=  rectLeftBounds.left && dotBounds.right <= rectLeftBounds.right)
  {
    dotSpeedY = (dotSpeedY + Math.random()) *-1;
    dotSpeedX = (dotSpeedX + Math.random())*-1;
  }
  // Rebotar contra las paredes de arriba o abajo
  else if ((dotSpeedY < 0 && dotBounds.top <= court.offsetTop) || (dotBounds.bottom>= courtBounds.bottom && dotSpeedY> 0)) {
    dotSpeedY = (dotSpeedY + Math.random()) *-1;
  }
  // salirse del court
  else if (dotBounds.left  <= courtBounds.left|| dotBounds.left+ dot.offsetWidth >= courtBounds.right) {
    dotKicked = false;
    start = false;
  }
  if (dotKicked) {
    requestAnimationFrame(animateDot);
  }
}

window.addEventListener('keydown', function(event) {
  switch(event.key) {
    case 'ArrowUp':
        gameSocket.send(JSON.stringify({
            'message': "UP"
        }));
      break;
    case 'ArrowDown':
        gameSocket.send(JSON.stringify({
            'message': "DOWN"
        }));
      break;
    case 'Enter':
      console.log("ENTER")
        gameSocket.send(JSON.stringify({
            'message': "ENTER"
        }));
        break;
    case 'w':
      gameSocket.send(JSON.stringify({
          'message': "W"
      }));
      break;
    case 's':
      gameSocket.send(JSON.stringify({
          'message': "S"
      }));
      break;
  }
});

window.addEventListener("keydown", function(e) {
  if(["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "Enter", "A", "S"].indexOf(e.code) > -1) {
      e.preventDefault();
  }
}, false);