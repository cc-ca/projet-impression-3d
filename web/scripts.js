const stopPrintingButton = document.getElementById("stop-printing");
const reloadButton = document.getElementById("reload");
const statusCircle = document.getElementById("status-circle");
const statusName = document.getElementById("status-name");
const printerImage = document.getElementById("printer-image");

const API_URL = "http://localhost:5000/";
const IMAGE_URL = "../photo_capturee.jpg";

const FETCH_INTERVAL = 15000; // 15 seconds

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
  try {
    await fetch(API_URL, {
      method: "POST",
    })
      .then((response) => response.json())
      .then((data) => {
        return;
      });
  } catch (error) {
    console.log("Error stopping printing: ", error);
  }
};

const fetchData = async () => {
  try {
    console.log("Fetching data...");
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
  } catch (error) {
    console.log("Error fetching data: ", error);
  }

  updateImage();
};

// const reFetchData = async () => {
//   await fetchData();
// };

function updateImage() {
  try {
    let timestamp = new Date().getTime();
    printerImage.src = `${IMAGE_URL}?${timestamp}`;
  } catch (error) {
    console.log("Error updating image: ", error);
  }
}

setInterval(async () => {
  await fetchData();
}, FETCH_INTERVAL);
fetchData();
