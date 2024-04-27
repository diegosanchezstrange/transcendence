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

/*
 * Function for the login form submit event
 * @return {boolean} - voiSd
 * */
function formSubmitLogin(form) {
  // e.preventDefault();

  let formData = new FormData(form);
  let body = {};
  let csrfToken;

  formData.forEach((value, key) => {
    if (key === "csrfmiddlewaretoken") csrfToken = value;
    body[key] = value;
  });

  body = JSON.stringify(body);

  fetch(form.getAttribute("action"), {
    method: form.getAttribute("method"),
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
      // if (!notificationsWebSocket)
      //   notficationsWebSocket = new NotificationsWebsocket();
      Router.changePage("/home/");
    })
    // TO DO: console error
    .catch(() => {
      addAlertBox(
        "Login failed!",
        "danger",
        document.getElementById("loginBox")
      );
    });

  return true;
}

function formSubmitRegister(form) {
  // e.preventDefault();

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

  let formData = new FormData(form);
  let body = {};
  let csrfToken;

  formData.forEach((value, key) => {
    if (key === "csrfmiddlewaretoken") csrfToken = value;
    if (key === "passwordRepeat") return;
    body[key] = value;
  });

  body = JSON.stringify(body);

  fetch(form.getAttribute("action"), {
    method: form.getAttribute("method"),
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
    // TO DO: console error
    .catch(() => {
      addAlertBox(
        "Registration failed!",
        "danger",
        document.getElementById("registerBox")
      );
    });
}

// Check if the forms exist on the page
// If they do, add event listeners to them

// document.getElementById("loginForm") &&
//   document
//     .getElementById("loginForm")
//     .addEventListener("submit", formSubmitLogin);
//
// document.getElementById("registerForm") &&
//   document
//     .getElementById("registerForm")
//     .addEventListener("submit", formSubmitRegister);
