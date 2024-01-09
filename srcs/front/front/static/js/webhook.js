function addNotificationBox(title, info, message) {
  const toastLiveExample = document.getElementById("liveToast");

  const newToast = toastLiveExample.cloneNode(true);

  newToast.id = "liveToast" + Math.floor(Math.random() * 1000);
  newToast.querySelector(".toast-body").innerHTML = message;
    newToast.querySelector(".toast-header-title").innerHTML = title;
    newToast.querySelector(".toast-header-info").innerHTML = info;


  document.querySelector(".toast-container").appendChild(newToast);

  newToast.addEventListener("hidden.bs.toast", function () {
    newToast.remove();
  });

  let toast = new bootstrap.Toast(newToast);

  toast.show();
}

class NotificationsWebsocket {
  constructor() {
    let token = null;
    if (Router.getJwt()) token = Router.getJwt();
    else return;

    // Add the token to the url as a query parameter
    this.socket = new WebSocket(
      NOTIFICATIONS_SOCKETS_HOST + "/ws/notifications/?token=" + token,
    );

    this.socket.onopen = () => {
      console.log("WebSocket Client Connected");
    };
    this.socket.onmessage = (message) => {
      console.log(message);
      let data = JSON.parse(message.data);
      console.log(data);
      addNotificationBox("New friend request", data["sender"], data["message"]);
      fill_friends_list(USERS_SERVICE_HOST + "/friends/");
    };
  }

  send(message) {
    if (this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(message);
    }
  }
}
