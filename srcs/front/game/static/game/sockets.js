

const gameSocket = new WebSocket(
    'ws://'
    + 'localhost:8000'
    + '/ws/game/');

gameSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(data);
};

gameSocket.onclose = function(e) {
    console.error('Game socket closed unexpectedly');
}

document.querySelector('#send').addEventListener('click', function(e) {
    const message = "Hello World";
    gameSocket.send(JSON.stringify({
        'message': message
    }));
});