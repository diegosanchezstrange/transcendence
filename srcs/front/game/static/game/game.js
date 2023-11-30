const dot = document.getElementById('dot');
const court = document.getElementById('court');
const rectangle_right = document.getElementById('rectangle-right');
const rectangle_left = document.getElementById('rectangle-left');
let pongCourtWidth = court.getBoundingClientRect().width;
let pongCourtHeight = court.getBoundingClientRect().height;
// center the dot inside the court
var dotX = pongCourtWidth / 2 + court.offsetLeft - dot.offsetWidth / 2;
var dotY = pongCourtHeight / 2 +court.offsetTop- dot.offsetHeight / 2;
let rectLeftPos = rectangle_left.getBoundingClientRect().top;
let rectRightPos = rectangle_right.getBoundingClientRect().top;
let top_rect = rectangle_left.getBoundingClientRect().top;
let dotKicked = false;
let start = true
let vel = 5.5;
Array.prototype.sample = function(){
  return this[Math.floor(Math.random()*this.length)];
}
var dirX = [1, -1].sample();
var dirY = [1, -1].sample();
let dotSpeedX = vel *dirX;
let dotSpeedY = vel*dirY;

dot.style.left = `${dotX}px`;
dot.style.top = `${dotY}px`;

const step = 12; 

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
    console.log("entro")
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
    console.log("PARED")
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
      moveRectangleRight(-step);
      break;
    case 'ArrowDown':
      moveRectangleRight(step);
      break;
    case 'Enter':
      kickDot();
      break;
    case 'w':
      moveRectangleLeft(-step);
      break;
    case 's':
      moveRectangleLeft(step);
      break;
  }
});

window.addEventListener("keydown", function(e) {
  if(["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "Enter", "A", "S"].indexOf(e.code) > -1) {
      e.preventDefault();
  }
}, false);