 function getCsrfToken() {
  let csrfToken = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, "csrftoken=".length) === "csrftoken=") {
        csrfToken = decodeURIComponent(cookie.substring("csrftoken=".length));
        break;
      }
    }
  }
  return csrfToken;
}


// /*
//  * Function to add an alert box to the page
//  * @param {string} message - The message to display in the alert box
//  * @param {string} type - The type of alert box to display
//  * @param {string} container - The container to add the alert box to
//  * @return {void}
//  * */
// function addAlertBox(message, type, container) {
//   let alert = document.createElement("div");
//
//   if (document.getElementById("alert")) {
//     document.getElementById("alert").remove();
//   }
//
//   alert.className = "alert alert-" + type;
//   alert.id = "alert";
//   alert.innerHTML = message;
//   container.prepend(alert);
// }

/*
 * Function for the login form submit event
 * @return {boolean} - voiSd
 * */
function formSubmitLogin(e) {
  e.preventDefault();

  let formData = new FormData(this);
  let body = {};
  let csrfToken;

  formData.forEach((value, key) => {
    if (key === "csrfmiddlewaretoken") csrfToken = value;
    body[key] = value;
  });

  body = JSON.stringify(body);

  fetch(this.getAttribute("action"), {
    method: this.getAttribute("method"),
    credentials: "include",
    headers: {
      "X-CSRFToken": csrfToken,
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: body,
  })
    .then((response) => {
      if (response.ok) {
        return response.json();
      }
      throw new Error("Network response was not ok.");
    })
    .then((text) => {
      // console.log(text);
      localStorage.setItem("token", text.access);
      notficationsWebSocket = new NotificationsWebsocket();
      Router.changePage("/home/");
    })
    .catch((error) => {
      console.log(error);
      addAlertBox(
        "Login failed!",
        "danger",
        document.getElementById("loginBox")
      );
    });
}

function formSubmitRegister(e) {
  e.preventDefault();

  // Get the input field
  //
  let password = document.getElementById("password");
  let passwordConfirm = document.getElementById("passwordRepeat");

  // Validate password
  if (password.value != passwordConfirm.value) {
    addAlertBox(
      "Passwords do not match!",
      "danger",
      document.getElementById("registerBox")
    );
    return;
  }

  let formData = new FormData(this);
  let body = {};
  let csrfToken;

  formData.forEach((value, key) => {
    if (key === "csrfmiddlewaretoken") csrfToken = value;
    if (key === "passwordRepeat") return;
    body[key] = value;
  });

  body = JSON.stringify(body);

  fetch(this.getAttribute("action"), {
    method: this.getAttribute("method"),
    credentials: "include",
    headers: {
      "X-CSRFToken": csrfToken,
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: body,
  })
    .then((response) => {
      if (response.ok) {
        return response.text();
      }
      throw new Error("Network response was not ok.");
    })
    .then((text) => {
      console.log(text);
      addAlertBox(
        "Registration successful!",
        "success",
        document.getElementById("registerBox")
      );
      Router.changePage("/login/");
    })
    .catch((error) => {
      console.log(error);
      addAlertBox(
        "Registration failed!",
        "danger",
        document.getElementById("registerBox")
      );
    });
}

// Check if the forms exist on the page
// If they do, add event listeners to them

document.getElementById("loginForm") &&
  document
    .getElementById("loginForm")
    .addEventListener("submit", formSubmitLogin);

document.getElementById("registerForm") &&
  document
    .getElementById("registerForm")
    .addEventListener("submit", formSubmitRegister);
