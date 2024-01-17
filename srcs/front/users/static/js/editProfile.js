const username = document.getElementById("profile-username");
const edit_username_button = document.getElementById("name-edit-button");
const end_button = document.getElementById("confirm-name-edit-button");
const avatar = document.getElementById("user-profile-avatar");
const edit_avatar_button = document.getElementById("img-edit-button");

edit_username_button.addEventListener("click", function() {
  edit_username_button.style.display = "none";
  end_button.style.display = "inline";
  username.contentEditable = true;
  username.style.backgroundColor = "rgba(54, 54, 71, 0.711)";
} );

end_button.addEventListener("click", function() {
  username.contentEditable = false;
  username.style.background = "transparent";
  end_button.style.display = "none";
  edit_username_button.style.display = "inline";
} )

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

function edit_username(e) {ƒ
  e.preventDefault();
  let new_username = username.value;

  formData.forEach((value, key) => {
    if (key === "csrfmiddlewaretoken") csrfToken = value;
    body[key] = value;
  });

  body = JSON.stringify(body);

  let headers = {
    "X-CSRFToken": csrfToken,
    Accept: "application/json",
    "Content-Type": "application/json",
  };

  if (Router.getJwt()) headers["Authorization"] = "Bearer " + Router.getJwt();

  fetch(this.getAttribute("action"), {
    method: this.getAttribute("method"),
    credentials: "include",
    headers: headers,
    body: body,
  })
    .then((response) => {
      if (response.ok) {
        return response.text();
      }
      throw new Error("Network response was not ok.");
    })
  }

//   let headers = {
//     "X-Requested-With": "XMLHttpRequest",
//     "Content-Type": "application/json",
//   };

//

//   fetch(this.getAttribute("action"), {
//     method: "PUT",
//     // credentials: "include",
//     headers: headers,
//   })
//     .then(async function (response) {
//       if (!response.ok) {
//         let res = await response.json();
//         throw new Error(res["detail"]);
//       }
//       return response.json();
//     })
//     .then(function (json) {
//       console.log(json["detail"]);
//     })
//     .catch(function (error) {
//       let container = document.getElementById("profile_username");
//       addAlertBox("Error: " + error.message, "danger", container);
//     });
// }

end_button.addEventListener("submit", edit_username);