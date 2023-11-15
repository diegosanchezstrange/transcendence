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
let dotKicked = false;
let dotSpeedX = 3.5;
let dotSpeedY = -3.5;

dot.style.left = `${dotX}px`;
dot.style.top = `${dotY}px`;

const step = 10; 

function moveRectangleRight(dx) {
  if (rectRightPos + dx < court.offsetTop || rectRightPos + dx + rectangle_right.offsetHeight > court.offsetTop + pongCourtHeight) {
    return;
  }
  rectRightPos += dx;
  rectangle_right.style.top = `${rectRightPos}px`;
}
function moveRectangleLeft(dx) {
  if (rectLeftPos + dx < court.offsetTop || rectLeftPos + dx + rectangle_left.offsetHeight > court.offsetTop + pongCourtHeight) {
    return;
  }
  rectLeftPos += dx;
  rectangle_left.style.top = `${rectLeftPos}px`;
}

function kickDot() {
  if (!dotKicked){
    dotX = pongCourtWidth / 2 + court.offsetLeft - dot.offsetWidth / 2;
    dotY = pongCourtHeight / 2 +court.offsetTop- dot.offsetHeight / 2;
    dot.style.left = `${dotX}px`;
    dot.style.top = `${dotY}px`;
    dotSpeedX = 3.5;
    dotSpeedY = -3.5;
    dotKicked = true;
    return;
  }
  dotX += dotSpeedX + Math.random()*2;
  dotY += dotSpeedY + Math.random()*2;
  dotKicked = true;
  animateDot();
}

function animateDot() {

  if (!dotKicked) {
    return;
  }
  dotX += dotSpeedX;
  dotY += dotSpeedY;
  if (dotY <= court.offsetTop || dotY + dot.offsetHeight>= court.offsetTop + pongCourtHeight) {
    dotSpeedY = dotSpeedY * -1 + Math.random();
  }
  dot.style.left = `${dotX}px`;
  dot.style.top = `${dotY}px`;

  let rectRightBounds = rectangle_right.getBoundingClientRect();
  let rectLeftBounds = rectangle_left.getBoundingClientRect();
  let courtBounds = court.getBoundingClientRect();
  let dotBounds = dot.getBoundingClientRect();

  if (dotBounds.left <= rectLeftBounds.right  && dotBounds.top >= rectLeftBounds.top + dot.offsetHeight/2 && dotBounds.bottom <= rectLeftBounds.bottom - dot.offsetHeight/2)
  {
    dotSpeedY = (dotSpeedY+ Math.random())*-1;
    dotSpeedX = (dotSpeedX+ Math.random())*-1;
  }

  if (dotBounds.left + dot.offsetWidth >= rectRightBounds.left && dotBounds.top >= rectRightBounds.top && dotBounds.bottom <= rectRightBounds.bottom)
  {
    dotSpeedY = (dotSpeedY + Math.random()) *-1;
    dotSpeedX = (dotSpeedX + Math.random())*-1;
  }
  /*
  if (dotY + dot.offsetHeight >= courtBounds.top || dotY - dot.offsetHeight <= courtBounds.bottom) {
    dotSpeedY *= -1;
    dotSpeedX *= -1;
  }
  */
  if (dotBounds.left  <= courtBounds.left|| dotBounds.left+ dot.offsetWidth >= courtBounds.right) {
    dotKicked = false;
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