const containers = {
  header: document.querySelector("header"),
  main: document.querySelector("main"),
  footer: document.querySelector("footer"),
  body: document.querySelector("body"),
};

class Router {
  constructor() {
    this.routes = {};
  }

  static insertHtml(html) {
    let parser = new DOMParser();
    let doc = parser.parseFromString(html, "text/html");

    Array.from(doc.body.children).forEach((child) => {
      if (
        child.nodeType === Node.ELEMENT_NODE &&
        child.tagName !== "SCRIPT" &&
        child.tagName.toLowerCase() in containers
      ) {
        // Replace the content of the container with the new content
        containers[child.tagName.toLowerCase()].innerHTML = child.innerHTML;
      } else if (child.tagName === "SCRIPT") {
        let newScript = document.createElement("script");

        if (child.src) newScript.src = child.src;
        else newScript.textContent = child.textContent;

        containers["body"].appendChild(newScript);
      }
    });
  }

  static changePage(url, popstate = false) {
    fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "text/html",
        "X-Requested-With": "XMLHttpRequest",
      },
    })
      .then((response) => response.text())
      .then((html) => {
        Router.insertHtml(html);
        if (!popstate) {
          history.pushState({ page: url }, "", url);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
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
  if (path) Router.changePage("/" + path);
  else Router.changePage("/home");
});
