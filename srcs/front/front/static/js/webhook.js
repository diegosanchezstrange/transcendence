class NotificationsWebsocket {
  constructor() {
    let token = null;
    if (Router.getJwt()) token = Router.getJwt();
    // this.socket = new WebSocket("ws://100.116.61.49:8082/ws/notifications/");
    // Add the token to the url as a query parameter
    this.socket = new WebSocket("ws://100.116.61.49:8082/ws/notifications/?token=" + token);

    this.socket.onopen = () => {
      console.log("WebSocket Client Connected");
    };
    this.socket.onmessage = (message) => {
      console.log(message);
    };
  }

  send(message) {
    if (this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(message);
    }
  }
}
