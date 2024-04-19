console.log("navbarUser.js loaded");
document.getElementById("friends_dropdown") &&
  document
    .getElementById("friends_dropdown")
    .addEventListener(
      "show.bs.dropdown",
      fill_friends_list(USERS_SERVICE_HOST + "/friends/"),
    );

document.getElementById("send_friend_request_form") &&
  document
    .getElementById("send_friend_request_form")
    .addEventListener("submit", send_friend_request);
