const stopPrintingButton = document.getElementById("stop-printing");
const reloadButton = document.getElementById("reload");
const statusCircle = document.getElementById("status-circle");
const statusName = document.getElementById("status-name");
const printerImage = document.getElementById("printer-image");
const circularDiagram = document.getElementById("circular-diagram");
const errorLimitRange = document.getElementById("error-limit-range");
const rangeValue = document.getElementById("range-value");

const host = window.location.href;
const formatedHost = host.endsWith("/") ? host.slice(0, -1) : host;

const API_URL = `${formatedHost}`;
const IMAGE_URL = "static/images/";

const FETCH_INTERVAL = 5000; // 5 seconds
let errorLimitRate = 0.75;

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

errorLimitRange.addEventListener("input", (event) => {
  rangeValue.textContent = event.target.value;
});

errorLimitRange.addEventListener("change", async (event) => {
  errorLimitRate = event.target.value;
  try {
    const response = await fetch(`${API_URL}/modify_threshold`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ confidence_threshold: errorLimitRate }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Failed to update threshold");
    }
  } catch (error) {
    console.log("Error updating error limit rate: ", error);
  }
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

        if (data.confidence_threshold) {
          errorLimitRate = data.confidence_threshold;
          errorLimitRange.value = errorLimitRate;
          rangeValue.textContent = errorLimitRate;
        }

        statusName.textContent =
          status.charAt(0).toUpperCase() + status.slice(1).toLowerCase();
        statusName.style.color = `var(--${MapStatusAndColor[status]})`;
        updateDiagram(data.error_rate);
        updateImage(data.image_name);
      });
  } catch (error) {
    console.log("Error fetching data: ", error);
  }
};

function updateImage(imageName) {
  try {
    printerImage.src = `${IMAGE_URL}${imageName}`;
  } catch (error) {
    console.log("Error updating image: ", error);
  }
}

function updateDiagram(errorRate) {
  try {
    const successRate = (1 - errorRate) * 100;
    const successSize = (successRate * 360) / 100;

    const orangeStart = 360 - (errorLimitRate * 360 - 1);
    const orangeEnd = orangeStart + 2;

    const redStart = successSize;
    const redEnd = 360;

    let gradient;
    if (
      errorRate === undefined ||
      errorRate === null ||
      typeof errorRate !== "number"
    ) {
      gradient = `
        conic-gradient(
          var(--gray) 0deg,
          var(--gray) 360deg
        )
      `;
    } else if (errorRate <= 1 - errorRate) {
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
  } catch (error) {
    console.log("Error updating diagram: ", error);
  }
}

setInterval(async () => {
  await fetchData();
}, FETCH_INTERVAL);
fetchData();
