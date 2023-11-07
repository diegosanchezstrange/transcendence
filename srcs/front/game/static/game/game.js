const dot = document.getElementById('dot');
const rectangle = document.getElementById('rectangle');
let rectangleX = window.innerWidth / 2 - 50;
let dotX = 50; 
let dotY = 80; 
let dotKicked = false;
let dotSpeedX = 5;
let dotSpeedY = -5;

dot.style.left = `${dotX}px`;
dot.style.top = `${dotY}px`;

const step = 10; 

function moveRectangle(dx) {
  rectangleX += dx;
  rectangle.style.left = `${rectangleX}px`;
}

function kickDot() {
  if (dotKicked) return;
  dotKicked = true;
  animateDot();
}

function animateDot() {
  if (!dotKicked) return;

  dotX += dotSpeedX;
  dotY += dotSpeedY;
  if (dotX <= 0 || dotX + dot.offsetWidth >= window.innerWidth) {
    dotSpeedX *= -1;
  }
  if (dotY <= 0) {
    dotSpeedY *= -1;
  }

  dot.style.left = `${dotX}px`;
  dot.style.top = `${dotY}px`;

  let rectBounds = rectangle.getBoundingClientRect();
  let dotBounds = dot.getBoundingClientRect();

  if (dotBounds.right > rectBounds.left && dotBounds.left < rectBounds.right &&
      dotBounds.bottom > rectBounds.top && dotBounds.top < rectBounds.bottom) {
    dotSpeedY *= -1;
    // dotSpeedX *= 1.1;
    // dotSpeedY *= 1.1;
  }

  if (dotY + dot.offsetHeight >= window.innerHeight) {
    dotKicked = false;
  }

  if (dotKicked) {
    requestAnimationFrame(animateDot);
  }
}

window.addEventListener('keydown', function(event) {
  switch(event.key) {
    case 'ArrowLeft':
      moveRectangle(-step);
      break;
    case 'ArrowRight':
      moveRectangle(step);
      break;
    case 'Enter':
      kickDot();
      break;
  }
});

window.addEventListener("keydown", function(e) {
  if(["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "Enter"].indexOf(e.code) > -1) {
      e.preventDefault();
  }
}, false);