const containers = {
  header: document.querySelector("header"),
  nav: document.querySelector("nav"),
  main: document.querySelector("main"),
  footer: document.querySelector("footer"),
  body: document.querySelector("body"),
};

/*
 * Function to add an alert box to the page
 * @param {string} message - The message to display in the alert box
 * @param {string} type - The type of alert box to display
 * @param {string} container - The container to add the alert box to
 * @return {void}
 * */
function addAlertBox(message, type, container) {
  let alert = document.createElement("div");

  if (document.getElementById("alert")) {
    document.getElementById("alert").remove();
  }

  alert.className = "alert alert-" + type;
  alert.id = "alert";
  alert.innerHTML = message;
  container.prepend(alert);
}

class Router {
  constructor() {
    this.routes = {};
  }

  static getJwt() {
    return localStorage.getItem("token");
  }

  static insertHtml(html) {
    let parser = new DOMParser();
    let doc = parser.parseFromString(html, "text/html");

    let chidlScrips = [];

    Array.from(doc.body.children).forEach((child) => {
      if (
        child.nodeType === Node.ELEMENT_NODE &&
        child.tagName !== "SCRIPT" &&
        child.tagName.toLowerCase() in containers
      ) {
        // Replace the content of the container with the new content
        child.childNodes.forEach((node) => {
          if (
            node.nodeType === Node.ELEMENT_NODE &&
            node.tagName === "SCRIPT"
          ) {
            let newScript = document.createElement("script");

            //remove the script from the child
            node.remove();

            if (node.src) newScript.src = node.src;
            else newScript.textContent = node.textContent;

            // document.body.appendChild(newScript);
            chidlScrips.push(newScript);
          }
        });
        containers[child.tagName.toLowerCase()].innerHTML = child.innerHTML;
        chidlScrips.forEach((node) => document.body.appendChild(node));
      } else if (child.tagName === "SCRIPT") {
        let newScript = document.createElement("script");

        if (child.src) newScript.src = child.src;
        else newScript.textContent = child.textContent;

        // containers["body"].appendChild(newScript);
        document.body.appendChild(newScript);
      }
    });
  }

  static changePage(url, popstate = false) {
    let headers = {
      "X-Requested-With": "XMLHttpRequest",
      "Content-Type": "text/html",
    };

    if (Router.getJwt()) headers["Authorization"] = "Bearer " + Router.getJwt();

    fetch(url, {
      method: "GET",
      headers: headers,
    })
      .then((response) => {
        if (response.status === 401) {
          throw new Error(response.status);
        }
        if (response.redirected) {
          url = new URL(response.url).pathname;
        }
        return response.text();
      })
      .then((html) => {
        Router.insertHtml(html);
        if (!popstate) {
          history.pushState({ page: url }, "", url);
        }
      })
      .catch((error) => {
        console.log(error.message);
        let errorCode = parseInt(error.message);
        if (errorCode === 401) {
          localStorage.removeItem("token");
          Router.changePage("/login");
        }
      });
  }
}

window.addEventListener("popstate", (event) => {
  if (event.state) {
    Router.changePage(location.pathname, true);
  }
});

document.addEventListener("DOMContentLoaded", async function () {
  // TODO: Check where the token should be safely stored
  // const token = localStorage.getItem("token");
  //
  // Get the token from the cookie and store it in localStorage
  let token = document.cookie
    .split("; ")
    .find((row) => row.startsWith("token="));

  if (token) {
    token = token.split("=")[1];
    localStorage.setItem("token", token);
    document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
  }

  if (path) Router.changePage("/" + path);
  else Router.changePage("/home");
});
