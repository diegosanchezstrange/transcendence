// Edit username

const username = document.getElementById("profile-username");
const edit_username_button = document.getElementById("name-edit-button");
const end_button = document.getElementById("confirm-name-edit-button");

edit_username_button.addEventListener("click", function() {
  edit_username_button.style.display = "none";
  end_button.style.display = "inline";
  username.contentEditable = true;
  username.style.backgroundColor = "rgba(54, 54, 71, 0.711)";
} );

end_button.addEventListener("click", function(e) {
  e.preventDefault();
  username.contentEditable = false;
  username.style.background = "transparent";
  end_button.style.display = "none";
  edit_username_button.style.display = "inline";
} )

end_button.addEventListener("click", function(e) {
  e.preventDefault();
  let new_username = username.value;

  let headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json",
  };

  if (Router.getJwt()) headers["Authorization"] = "Bearer " + Router.getJwt();

  fetch(USERS_SERVICE_HOST + "/profile/edit/", {
    method: "PUT",
    headers: headers,
  })
    .then((response) => {
      if (response.ok) {
        return response.text();
      }
      throw new Error("Network response was not ok.");
    })
  })


// Edit profile image

const avatar = document.getElementById("user-profile-avatar");
const edit_avatar_button = document.getElementById("img-edit-button");

edit_avatar_button.addEventListener("click", function() {
  
  let headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json",
  };
  
  if (Router.getJwt()) headers["Authorization"] = "Bearer " + Router.getJwt();
  
  fetch(USERS_SERVICE_HOST + "/users/upload/", {
    method: "PUT",
    headers: headers,
  })
})
