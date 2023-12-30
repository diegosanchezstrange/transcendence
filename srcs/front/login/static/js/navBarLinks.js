function logout() {
  localStorage.removeItem("token");
  Router.changePage("/home/");
}
