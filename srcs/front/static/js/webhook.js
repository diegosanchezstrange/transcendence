function addNotificationBox(title, message) {
  const toastLiveExample = document.getElementById("liveToast");

  const newToast = toastLiveExample.cloneNode(true);

  newToast.id = "liveToast" + Math.floor(Math.random() * 1000);
  newToast.querySelector(".toast-body").innerHTML = message;
  newToast.querySelector(".toast-header-title").innerHTML = title;

  document.querySelector(".toast-container").appendChild(newToast);

  newToast.addEventListener("hidden.bs.toast", function () {
    newToast.remove();
  });

  let toast = new bootstrap.Toast(newToast);

  toast.show();
}

const NotificationType = {
    Sent: 1,
    Accepted: 2,
    Rejected: 3,
    Removed: 4,
    NameChanged: 5,
}

function changeNames(userId, newName) {
  const namesToChange = document.getElementsByClassName(`change_name_${userId}`);
  for (let i = 0; i < namesToChange.length; i++) {
    namesToChange[i].innerText = newName
  }
}

class NotificationsWebsocket {
  constructor() {
    let token = null;
    if (Router.getJwt()) token = Router.getJwt();
    else return;

    // Add the token to the url as a query parameter
    this.socket = new WebSocket(
      NOTIFICATIONS_SOCKETS_HOST + "/ws/notifications/?token=" + token
    );

    this.socket.onopen = () => {
      console.log("WebSocket Client Connected");
    };
    this.socket.onmessage = (message) => {
      let data = JSON.parse(message.data)["message"];
      console.log(data)
      switch (data["ntype"]) {
        case NotificationType.NameChanged:
          changeNames(data["sender"]["id"],data["message"])
          break;
        default:
          addNotificationBox("New friend request", data["message"]);
          fill_friends_list(USERS_SERVICE_HOST + "/friends/");
          break;
      }
    };
  }

  send(message) {
    if (this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(message);
    }
  }
}
