document.addEventListener("DOMContentLoaded", function () {
  const token = localStorage.getItem("token");
  let url;

  if (token) {
    // TODO: fetch home page partial
    url = "/home";
  } else {
    url = "/login";
  }
  fetch(url)
    .then((response) => response.text())
    .then((html) => {
      document.querySelector("main").innerHTML = html;
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
