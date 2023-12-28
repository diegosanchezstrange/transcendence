// import Router from "./spa.js";

document.getElementById("logoutButton") &&
  document.getElementById("logoutButton").addEventListener("click", () => {
    localStorage.removeItem("token");
    Router.changePage("/home/");
  });

function logout() {
  localStorage.removeItem("token");
  Router.changePage("/home/");
}
