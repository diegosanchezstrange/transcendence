function logout() {
  localStorage.removeItem("token");
  Router.changePage("/home/");
  return false;
}

function profile_link() {
  Router.changePage("/profile/");
  return false;
}

function home_link() {
  Router.changePage("/home/");
  return false;
}

function friends_link() {
  Router.changePage("/friends/");
  return false;
}

function send_friend_request(e) {
  e.preventDefault();
  let username_input = document.getElementById("username_input");
  let username = username_input.value;
  let headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json",
  };

  if (Router.getJwt()) headers["Authorization"] = "Bearer " + Router.getJwt();

  fetch(this.getAttribute("action"), {
    method: "POST",
    // credentials: "include",
    headers: headers,
    body: JSON.stringify({
      send_to: username,
    }),
  })
    .then(async function (response) {
      if (!response.ok) {
        let res = await response.json();
        throw new Error(res["detail"]);
      }
      return response.json();
    })
    .then(function (json) {
      // console.log(json["detail"]);
    })
    .catch(function (error) {
      let container = document.getElementById("friends_requests");
      addAlertBox("Error: " + error.message, "danger", container);
    });
}

function accept_friend_req(e) {
  let friend_name = e.target.parentElement.firstChild.innerHTML;

  let headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json",
  };

  if (Router.getJwt()) headers["Authorization"] = "Bearer " + Router.getJwt();

  fetch(this.action, {
    method: "POST",
    // credentials: "include",
    headers: headers,
    body: JSON.stringify({
      sender: friend_name,
    }),
  })
    .then(function (response) {
      if (response.ok) fill_friends_list(USERS_SERVICE_HOST + "/friends/");
    })
    .catch(function (error) {
      console.log(error);
    });
}

function reject_friend_req(e) {
  let friend_name = e.target.parentElement.firstChild.innerHTML;

  let headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json",
  };

  if (Router.getJwt()) headers["Authorization"] = "Bearer " + Router.getJwt();

  fetch(this.action, {
    method: "POST",
    // credentials: "include",
    headers: headers,
    body: JSON.stringify({
      sender: friend_name,
    }),
  })
    .then(function (response) {
      if (response.ok) fill_friends_list(USERS_SERVICE_HOST + "/friends/");
    })
    .catch(function (error) {
      console.log(error);
    });
}

function remove_friend_req(e) {
  let friend_name = e.target.parentElement.firstChild.innerHTML;

  let headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json",
  };

  if (Router.getJwt()) headers["Authorization"] = "Bearer " + Router.getJwt();

  fetch(this.action, {
    method: "DELETE",
    // credentials: "include",
    headers: headers,
    body: JSON.stringify({
      friend_name: friend_name,
    }),
  })
    .then(function (response) {
      if (response.ok) fill_friends_list(USERS_SERVICE_HOST + "/friends/");
    })
    .catch(function (error) {
      console.log(error);
    });
}

function challenge_friend(e) {
  let friend_name = e.target.parentElement.firstChild.innerHTML;
  let headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json",
  };

  if (Router.getJwt()) headers["Authorization"] = "Bearer " + Router.getJwt();

  fetch(GAME_SERVICE_HOST + "/challenge/", {
    method: "POST",
    // credentials: "include",
    headers: headers,
    body: JSON.stringify({
      opponent: friend_name,
    }),
  })
    .then(function (response) {
      if (response.ok) {
        Router.changePage("/pong/?opponent=" + friend_name);
      }
    })
    .catch(function (error) {
      console.log(error);
    });
}

function accept_game_req(e) {
  let invite_id = e.target.parentElement.firstChild.id;

  let headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json",
  };

  if (Router.getJwt()) headers["Authorization"] = "Bearer " + Router.getJwt();

  fetch(this.action, {
    method: "POST",
    // credentials: "include",
    headers: headers,
    body: JSON.stringify({
      invite_id: invite_id,
    }),
  })
    .then(function (response) {
      if (response.ok) fill_friends_list(USERS_SERVICE_HOST + "/friends/");
    })
    .catch(function (error) {
      console.log(error);
    });
}

function reject_game_req(e) {
  let invite_id = e.target.parentElement.firstChild.id;

  let headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json",
  };

  if (Router.getJwt()) headers["Authorization"] = "Bearer " + Router.getJwt();

  fetch(this.action, {
    method: "POST",
    // credentials: "include",
    headers: headers,
    body: JSON.stringify({
      invite_id: invite_id,
    }),
  })
    .then(function (response) {
      if (response.ok) fill_friends_list(USERS_SERVICE_HOST + "/friends/");
    })
    .catch(function (error) {
      console.log(error);
    });
}

function fill_friends_list(friends_list_url) {
  let friends_list = document.getElementById("friends_list");
  // let friends;

  let headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json",
  };

  if (Router.getJwt()) headers["Authorization"] = "Bearer " + Router.getJwt();

  fetch(friends_list_url + "requests/", {
    method: "GET",
    // credentials: "include",
    headers: headers,
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (json) {
      if (json["detail"].length != 0) {
        let friend_req_list = document.getElementById("friends_requests");
        json["detail"].forEach(function (friend) {
          // Accept button
          let accept_button = document.createElement("button");
          accept_button.classList = ["btn btn-success p-1 m-2"];
          accept_button.textContent = "Accept";
          accept_button.action = friends_list_url + "requests/accept/";
          accept_button.addEventListener("click", accept_friend_req);

          // Reject button
          let reject_button = document.createElement("button");
          reject_button.classList = ["btn btn-danger p-1 m-2"];
          reject_button.textContent = "Decline";
          reject_button.action = friends_list_url + "requests/reject/";
          reject_button.addEventListener("click", reject_friend_req);

          // Friend name
          let friend_request = document.createElement("span");
          let friend_name = document.createElement("p");
          friend_request.id = "friend-request";
          reject_button.id = "reject-button";
          friend_name.id = "friend-request-name";
          friend_name.innerHTML = friend;
          friend_request.appendChild(friend_name);
          friend_request.appendChild(accept_button);
          friend_request.appendChild(reject_button);
          friend_req_list.appendChild(friend_request);
        });
      } else {
        let friend_req_list = document.getElementById("friends_requests");
        friend_req_list.innerHTML = "";
      }
    })
    .catch(function (error) {
      console.log(error);
    });

  fetch(GAME_SERVICE_HOST + "/challenges/" + "?status=PENDING", {
    method: "GET",
    headers: headers,
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (json) {
      if (json["detail"].length != 0) {
        let games_list = document.getElementById("games_requests");
        json["detail"].forEach(function (game) {
          // Accept button
          let accept_button = document.createElement("button");
          accept_button.classList = ["btn btn-success p-1 m-2"];
          accept_button.textContent = "Accept";
          accept_button.action = GAME_SERVICE_HOST + "/challenge/accept/";
          accept_button.addEventListener("click", accept_game_req);

          // Reject button
          let reject_button = document.createElement("button");
          reject_button.classList = ["btn btn-danger p-1 m-2"];
          reject_button.textContent = "Decline";
          reject_button.action = GAME_SERVICE_HOST + "/challenge/reject/";
          reject_button.addEventListener("click", reject_game_req);

          // Opponent name
          let game_request = document.createElement("span");
          let opponent_name = document.createElement("p");

          let opponent = game["sender"];

          game_request.id = game["id"];
          opponent_name.innerHTML = opponent;
          game_request.appendChild(opponent_name);
          game_request.appendChild(accept_button);
          game_request.appendChild(reject_button);
          games_list.appendChild(game_request);
        });
      } else {
        let games_list = document.getElementById("games_requests");
        games_list.innerHTML = "";
      }
    })
    .catch(function (error) {
      console.log(error);
    });

  fetch(friends_list_url, {
    method: "GET",
    // credentials: "include",
    headers: headers,
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (json) {
      if (json["detail"].length === 0) {
        friends_list.innerHTML = "You have no friends :(";
      } else {
        friends_list.innerHTML = "";
        json["detail"].forEach(function (friend) {
          let friend_request = document.createElement("li");
          let friend_name = document.createElement("p");
          let remove_button = document.createElement("button");
          let challenge_button = document.createElement("button");

          friend_name.innerHTML = friend;

          remove_button.classList = ["btn btn-danger"];
          remove_button.action = friends_list_url;
          remove_button.addEventListener("click", remove_friend_req);

          challenge_button.classList = ["btn btn-primary"];
          challenge_button.innerHTML = "<i class='fa-solid fa-chess'></i>";
          challenge_button.addEventListener("click", challenge_friend);

          friend_request.appendChild(friend_name);
          friend_request.appendChild(challenge_button);
          friend_request.appendChild(remove_button);
          friends_list.appendChild(friend_request);
        });
      }
    })
    .catch(function (error) {
      console.log(error);
    });

  // for (let i = 0; i < friends.length; i++) {
  //     let friend = friends[i];
  //     let friend_li = document.createElement("li");
  //     let friend_link = document.createElement("a");
  //
  //     friend_link.href = "/profile/" + friend.username + "/";
  //     friend_link.innerHTML = friend.username;
  //
  //     friend_li.appendChild(friend_link);
  //     friends_list.appendChild(friend_li);
  // }
}

// window.onload = function () {
//   let profile_link = document.getElementById("profile_link");
//
//   let fiends_link = document.getElementById("fiends_link");
//
//   profile_link.onclick = function () {
//     Router.changePage("/profile/");
//
//     return false;
//   };
//
//   fiends_link.onclick = function () {
//     Router.changePage("/friends/");
//     return false;
//   };
// };
