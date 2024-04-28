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
async function addAlertBox(message, type, container, timeout = -1) {
  let alert = document.createElement("div");

  if (document.getElementById("alert")) {
    document.getElementById("alert").remove();
  }

  alert.className = "alert alert-" + type;
  alert.id = "alert";
  alert.innerHTML = message;
  container.prepend(alert);

  if (timeout > 0) {
    await new Promise((resolve) => setTimeout(resolve, timeout));
    alert.remove();
  }

  return alert;
}

class Router {
  // Variable to store the scripts that have been loaded
  static scripts = {};

  static getJwt() {
    return localStorage.getItem("token");
  }

  static async refreshToken() {
    let token = localStorage.getItem("token");
    let refreshToken = localStorage.getItem("refreshToken");

    if (token && refreshToken) {
      let body = {
        refresh: refreshToken,
      };

      let refreshData = await ft_fetch(
        LOGIN_SERVICE_HOST + "/auth/login/refresh/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(body),
        }
      );

      if (refreshData.status === 401) {
        localStorage.removeItem("token");
        localStorage.removeItem("refreshToken");
        if (notificationsWebSocket) {
          notificationsWebSocket.close();
          notificationsWebSocket = null;
        }
        Router.changePage("/login");
      } else {
        let data = await refreshData.json();
        localStorage.setItem("token", data.access);
      }
    }
  }

  static getUsername() {
    let token = localStorage.getItem("token");
    if (token) {
      let payload = token.split(".")[1];
      payload = atob(payload);
      payload = JSON.parse(payload);
      return payload.username;
    }
    return null;
  }

  static getUserId() {
    let token = localStorage.getItem("token");
    if (token) {
      let payload = token.split(".")[1];
      payload = atob(payload);
      payload = JSON.parse(payload);
      return payload.user_id;
    }
    return null;
  }

  static changePageEventDispat(newUrl) {
    let event = new CustomEvent("change-page", {
      detail: {
        newPage: newUrl,
      },
    });

    window.dispatchEvent(event);
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
            node.tagName === "SCRIPT" &&
            !(child.src in Router.scripts)
          ) {
            let newScript = document.createElement("script");

            //remove the script from the child
            node.remove();

            if (node.src) newScript.src = node.src;
            else newScript.textContent = node.textContent;

            // document.body.appendChild(newScript);
            chidlScrips.push(newScript);
            Router.scripts[child.src] = newScript;
          }
        });
        containers[child.tagName.toLowerCase()].innerHTML = child.innerHTML;
        chidlScrips.forEach((node) => document.body.appendChild(node));
      } else if (
        child.tagName === "SCRIPT" &&
        child.src &&
        !(child.src in Router.scripts)
      ) {
        let newScript = document.createElement("script");

        if (child.src) newScript.src = child.src;
        else newScript.textContent = child.textContent;

        // containers["body"].appendChild(newScript);
        document.body.appendChild(newScript);
        Router.scripts[child.src] = newScript;
      }
    });
  }

  static changePage(url, popstate = false) {
    let headers = {
      "X-Requested-With": "XMLHttpRequest",
      "Content-Type": "text/html",
    };

    if (Router.getJwt()) headers["Authorization"] = "Bearer " + Router.getJwt();

    ft_fetch(url, {
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
        if (!notificationsWebSocket && Router.getJwt()) {
          notificationsWebSocket = new NotificationsWebsocket();
        }
        Router.changePageEventDispat(url);
      })
      // TO DO: console error
      .catch((error) => {
        let errorCode = parseInt(error.message);
        if (errorCode === 401) {
          if (notificationsWebSocket) {
            notificationsWebSocket.close();
            notificationsWebSocket = null;
          }
        }
      });
  }
}

async function ft_fetch(url, options) {
  const response = await fetch(url, options);

  if (response.status === 401) {
    await Router.refreshToken();

    if (!options.headers) {
      options.headers = {};
    }
    options.headers.Authorization = "Bearer " + localStorage.getItem("token");

    return await fetch(url, options);
  }

  return response;
}

window.addEventListener("popstate", (event) => {
  if (event.state) {
    Router.changePage(location.pathname, true);
  }
});

document.addEventListener("DOMContentLoaded", async function () {
  // TODO: Check where the token should be safely stored
  // const token = localStorage.getItem("token");

  // window.ft_fetch = async function (url, options) {
  //   const token = localStorage.getItem("token");
  //   if (token) {
  //     if (!options.headers) {
  //       options.headers = {};
  //     }
  //     options.headers.Authorization = "Bearer " + token;
  //   }
  //
  //   try {
  //     let response = await originalft_fetch(url, options);
  //     console.log(response);
  //     return response;
  //   } catch (error) {
  //     console.log(error);
  //     if (response.status === 401) {
  //       await Router.refreshToken();
  //
  //       options.headers.Authorization =
  //         "Bearer " + localStorage.getItem("token");
  //       return originalft_fetch(url, options);
  //     }
  //   }
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
