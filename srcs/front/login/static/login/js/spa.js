document.addEventListener("DOMContentLoaded", async function () {
  // TODO: Check where the token should be safely stored
  const token = localStorage.getItem("token");
  let url;

  if (token) url = "/home";
  else url = "/login";

  fetch(url)
    .then((response) => response.text())
    .then((html) => {
      document.querySelector("main").innerHTML = "";
      let parser = new DOMParser();
      let doc = parser.parseFromString(html, "text/html");
      let container = document.querySelector("main");

      Array.from(doc.body.children).forEach((child) => {
        if (child.nodeType === Node.ELEMENT_NODE && child.tagName !== "SCRIPT")
          container.appendChild(child.cloneNode(true));
        else if (child.tagName === "SCRIPT") {
          let newScript = document.createElement("script");

          if (child.src) newScript.src = child.src;
          else newScript.textContent = child.textContent;

          container.appendChild(newScript);
        }
      });
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
