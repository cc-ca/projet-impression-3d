const stopPrintingButton = document.getElementById("stop-printing");
const reloadButton = document.getElementById("reload");
const statusCircle = document.getElementById("status-circle");
const statusName = document.getElementById("status-name");
const printerImage = document.getElementById("printer-image");

const API_URL = "http://TODEFINE:3000/";
const IMAGE_URL = "http://TODEFINE:3000/text.fr";

const MapStatusAndColor = {
  OFF: "gray",
  IDLE: "blue",
  ERROR: "red",
  CORRECT: "green",
  STOP: "red",
  ISSUE: "orange",
  WARMUP: "green",
};

stopPrintingButton.addEventListener("click", async () => {
  await stopPrinting();
  await fetchData();
});

reloadButton.addEventListener("click", async () => {
  await fetchData();
});

const stopPrinting = async () => {
  await fetch(API_URL, {
    method: "POST",
  })
    .then((response) => response.json())
    .then((data) => {
      return;
    });
};

const fetchData = async () => {
  await fetch(API_URL)
    .then((response) => response.json())
    .then((data) => {
      const status = Object.keys(data.states).find(
        (key) => data.states[key] === true
      );
      statusCircle.style.setProperty(
        "--circleColor",
        `var(--${MapStatusAndColor[status]})`
      );
      statusName.textContent =
        status.charAt(0).toUpperCase() + status.slice(1).toLowerCase();
      statusName.style.color = `var(--${MapStatusAndColor[status]})`;
    });

  updateImage();
};

const reFetchData = async () => {
  await fetchData();
  setInterval(() => {
    reFetchData();
  }, 5000);
};

function updateImage() {
  let timestamp = new Date().getTime();
  printerImage.src = `${IMAGE_URL}?${timestamp}`;
}

reFetchData();
