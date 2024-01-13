const username = document.getElementById("profile-username");
const edit_button = document.getElementById("name-edit-button");
const end_button = document.getElementById("confirm-name-edit-button");

edit_button.addEventListener("click", function() {
  edit_button.style.display = "none";
  end_button.style.display = "inline";
  username.contentEditable = true;
  username.style.backgroundColor = "rgba(54, 54, 71, 0.711)";
} );

end_button.addEventListener("click", function() {
  username.contentEditable = false;
  username.style.background = "transparent";
  end_button.style.display = "none";
  edit_button.style.display = "inline";
} )

function edit_username(e) {
  e.preventDefault();
  let new_username = username.value;
  let headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json",
  };

  if (Router.getJwt()) headers["Authorization"] = "Bearer " + Router.getJwt();
}

end_button.addEventListener("submit", edit_username);