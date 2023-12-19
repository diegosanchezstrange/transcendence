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

function formSubmit(e) {
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
        return response.text();
      }
      throw new Error("Network response was not ok.");
    })
    .then((text) => {
      console.log(text);
      let loginContainer = document.getElementById("loginBox");

      if (document.getElementById("alert")) {
        document.getElementById("alert").remove();
      }

      let alert = document.createElement("div");
      alert.className = "alert alert-success";
      alert.id = "alert";
      alert.innerHTML = "Login successful!";
      loginContainer.prepend(alert);
    })
    .catch((error) => {
      console.log(error);
      let loginContainer = document.getElementById("loginBox");

      if (document.getElementById("alert")) {
        document.getElementById("alert").remove();
      }

      let alert = document.createElement("div");
      alert.className = "alert alert-danger";
      alert.id = "alert";
      alert.innerHTML = "Login failed!";
      loginContainer.prepend(alert);
    });
}

document.getElementById("loginForm").addEventListener("submit", formSubmit);
