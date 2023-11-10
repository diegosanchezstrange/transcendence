document.addEventListener("DOMContentLoaded", async function () {
  // TODO: Check where the token should be safely stored
  const token = localStorage.getItem("token");
  let url;

  if (token) url = "/home";
  else url = "/login";

  fetch(url)
    .then((response) => response.text())
    .then((html) => {
      document.querySelector("main").innerHTML = html;
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
