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