const stopPrintingButton = document.getElementById("stop-printing");
const reloadButton = document.getElementById("reload");
const statusCircle = document.getElementById("status-circle");
const statusName = document.getElementById("status-name");
const printerImage = document.getElementById("printer-image");
const circularDiagram = document.getElementById("circular-diagram");

const host = window.location.href;
const formatedHost = host.endsWith("/") ? host.slice(0, -1) : host;

const API_URL = `${formatedHost}`;
const IMAGE_URL = "static/images/photo_capturee.jpg";

const FETCH_INTERVAL = 5000; // 5 seconds

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
    await fetch(`${API_URL}/stop`, {
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
    await fetch(`${API_URL}/status`)
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
        updateDiagram(data.error_rate);
      });
  } catch (error) {
    console.log("Error fetching data: ", error);
  }

  updateImage();
};

function updateImage() {
  try {
    printerImage.src = `${IMAGE_URL}`;
  } catch (error) {
    console.log("Error updating image: ", error);
  }
}

function updateDiagram(errorRate) {
  try {
    const MAX_ERROR_RATE = 0.75; // Maximum error rate allowed (50%)

    const successRate = (1 - errorRate) * 100;
    const successSize = (successRate * 360) / 100;

    console.log("Success rate: ", successRate);
    console.log("Success size: ", successSize);

    const orangeStart = MAX_ERROR_RATE * 360 - 1;
    const orangeEnd = orangeStart + 2;

    console.log("Orange start: ", orangeStart);
    console.log("Orange end: ", orangeEnd);

    const redStart = successSize;
    const redEnd = 360;

    console.log("Red start: ", redStart);
    console.log("Red end: ", redEnd);

    let gradient;
    if (errorRate <= 1 - MAX_ERROR_RATE) {
      gradient = `
        conic-gradient(
          var(--green) 0deg,
          var(--green) ${orangeStart}deg,
          var(--orange) ${orangeStart}deg,
          var(--orange) ${orangeEnd}deg,
          var(--green) ${orangeEnd}deg,
          var(--green) ${successSize}deg,
          var(--red) ${successSize}deg,
          var(--red) 360deg
        )
      `;
    } else {
      gradient = `
        conic-gradient(
          var(--green) 0deg,
          var(--green) ${redStart}deg,
          var(--red) ${redStart}deg,
          var(--red) ${orangeStart}deg,
          var(--orange) ${orangeStart}deg,
          var(--orange) ${orangeEnd}deg,
          var(--red) ${orangeEnd}deg,
          var(--red) ${redEnd}deg
        )
      `;
    }

    // Update the background of the circular diagram
    circularDiagram.style.background = gradient;
    console.log("Diagram updated", gradient);
  } catch (error) {
    console.log("Error updating diagram: ", error);
  }
}

setInterval(async () => {
  await fetchData();
}, FETCH_INTERVAL);
fetchData();
