function logout() {
  localStorage.removeItem("token");
  Router.changePage("/home/");
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
        .then(function (response) {
            return response.json();
        })
        .then(function (json) {
            console.log(json);
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

  fetch(friends_list_url, {
    method: "GET",
    // credentials: "include",
    headers: headers,
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (json) {
      console.log(json);
      if (json["detail"].length === 0) {
        friends_list.innerHTML = "You have no friends :(";
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
