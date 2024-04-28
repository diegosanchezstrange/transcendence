// Edit username

const username = document.getElementById("profile-username");
const edit_username_button = document.getElementById("name-edit-button");
const end_button = document.getElementById("confirm-name-edit-button");

function editUsername() {
  edit_username_button.style.display = "none";
  end_button.style.display = "inline";

  username.removeAttribute("disabled");
  username.style.backgroundColor = "rgba(54, 54, 71, 0.711)";
  username.focus();
  username.setSelectionRange(username.value.length, username.value.length);
}

function confirmUsernameHandler1() {
  // e.preventDefault();
  end_button.style.display = "none";
  edit_username_button.style.display = "inline";

  username.setAttribute("disabled", "");
  username.style.background = "transparent";
}

function confirmUsernameHandler2() {
  // e.preventDefault();
  let headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json",
  };

  if (Router.getJwt()) headers["Authorization"] = "Bearer " + Router.getJwt();

  let body = {
    username: username.value,
  };
  body = JSON.stringify(body);

  ft_fetch(USERS_SERVICE_HOST + "/profile/edit/", {
    method: "PUT",
    headers: headers,
    body: body,
  }).then((response) => {
    if (!response.ok) {
      response.json().then(async (json) => {
        username.value = json.original_name;
        await addAlertBox(
          json.detail,
          "danger",
          document.getElementById("username-form"),
          3000,
        );
      });
    } else {
      response.json().then(async (json) => {
        if (json.original_name !== username.value) {
          await addAlertBox(
            "Username changed!",
            "success",
            document.getElementById("username-form"),
            2000,
          );
        }
      });
    }
  });
}

// Edit profile image

const avatar = document.getElementById("user-profile-avatar");
const edit_avatar_button = document.getElementById("img-edit-button");
const profile_picture_input = document.getElementById("profile-picture-input");
const profile_picture_form = document.getElementById("profile-picture-form");

function changeProfilePicture() {
  if (!profile_picture_input.files[0]) return;
  let headers = {
    "X-Requested-With": "XMLHttpRequest",
  };

  if (Router.getJwt()) headers["Authorization"] = "Bearer " + Router.getJwt();

  let body = new FormData();
  body.append("profile_pic", profile_picture_input.files[0]);

  ft_fetch(USERS_SERVICE_HOST + "/users/upload/", {
    method: "POST",
    headers: headers,
    body: body,
  })
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      let timestamp = new Date().getTime();
      avatar.src = json.url + "?t=" + timestamp;
    });
}
