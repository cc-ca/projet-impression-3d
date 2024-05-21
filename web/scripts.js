const stopPrintingButton = document.getElementById("stop-printing");
const reloadButton = document.getElementById("reload");
const statusCircle = document.getElementById("status-circle");
const statusName = document.getElementById("status-name");

const API_URL = "http://TODEFINE:3000/";

const MapStatusAndColor = {
  OFF: "red",
  IDLE: "yellow",
  error: "red",
  CORRECT: "green",
  STOP: "red",
  ISSUE: "yellow",
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
      statusCircle.style.backgroundColor = `var(--${MapStatusAndColor[status]})`;
      statusName.innerText = status;
      statusName.style.color = `var(--${MapStatusAndColor[status]})`;
    });
};

const reFetchData = async () => {
  await fetchData();
  setInterval(() => {
    reFetchData();
  }, 5000);
};

reFetchData();
