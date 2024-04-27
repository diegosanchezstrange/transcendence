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
  ImgChanged: 6,
  UserOnline: 7,
  UserOffline: 8,
  UserOnlineNotification: 9,
  UserOfflineNotification: 10,
  GameFound: 11,
  GameInvite: 12,
  TournamentFound: 13,
};

function changeNames(userId, newName) {
  const namesToChange = document.getElementsByClassName(
    `change_name_${userId}`
  );
  for (let i = 0; i < namesToChange.length; i++) {
    namesToChange[i].innerText = newName;
  }
}

function changeImgs(userId, newUrl) {
  const imgsToChange = document.getElementsByClassName(`change_img_${userId}`);
  for (let i = 0; i < imgsToChange.length; i++) {
    let timestamp = new Date().getTime();
    imgsToChange[i].src = newUrl + "?t=" + timestamp;
  }
}

function changeStatus(userId, style, content) {
  const statusToChange = document.getElementsByClassName(
    `change_status_${userId}`
  );
  for (let i = 0; i < statusToChange.length; i++) {
    statusToChange[i].style = style;
    statusToChange[i].innerHTML = content;
  }
}

class NotificationsWebsocket {
  constructor() {
    let token = null;
    if (Router.getJwt()) token = Router.getJwt();
    else return;

    // Add the token to the url as a query parameter
    this.socket = new WebSocket(
      NOTIFICATIONS_SOCKETS_HOST + "/notifications/?token=" + token
    );

    this.socket.onopen = () => {
      console.log("WebSocket Client Connected");
    };
    this.socket.onmessage = (message) => {
      let data = JSON.parse(message.data)["message"];
      switch (data["ntype"]) {
        case NotificationType.NameChanged:
          changeNames(data["sender"]["id"], data["message"]);
          fill_friends_list(USERS_SERVICE_HOST + "/friends/");
          break;
        case NotificationType.ImgChanged:
          changeImgs(data["sender"]["id"], data["message"]);
          break;
        case NotificationType.UserOnlineNotification:
          addNotificationBox("Event", data["message"]);
          fill_friends_list(USERS_SERVICE_HOST + "/friends/");
          break;
        case NotificationType.UserOfflineNotification:
          addNotificationBox("Event", data["message"]);
          fill_friends_list(USERS_SERVICE_HOST + "/friends/");
          break;
        case NotificationType.UserOnline:
          changeStatus(
            data["sender"]["id"],
            "color: rgb(150, 200, 150);",
            "online"
          );
          break;
        case NotificationType.UserOffline:
          changeStatus(
            data["sender"]["id"],
            "color: rgb(105, 105, 105);",
            "offline"
          );
          break;
        case NotificationType.GameFound:
          addNotificationBox("Event", data["message"]);
          let opponent = data["sender"]["username"];
          Router.changePage("/pong/" + "?opponent=" + opponent);
          break;
        case NotificationType.TournamentFound:
          addNotificationBox("Event", data["message"]);
          let tournament = data["tournament_id"];
          Router.changePage("/lobby/" + "?tournament=" + tournament);
          break;
        default:
          addNotificationBox("Message", data["message"]);
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
