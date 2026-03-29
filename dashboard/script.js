const API = "http://127.0.0.1:5000";

let chart;
let labels = [];
let dataPoints = [];
const totalSeats = 10;

// ---------------- CREATE SEATS ----------------
function createSeats() {
    const container = document.getElementById("seats");

    for (let i = 0; i < totalSeats; i++) {
        const seat = document.createElement("div");
        seat.className = "seat free";
        seat.id = "seat-" + i;
        container.appendChild(seat);
    }
}

// ---------------- UPDATE SEATS ----------------
function updateSeats(occupied) {
    for (let i = 0; i < totalSeats; i++) {
        const seat = document.getElementById("seat-" + i);

        if (i < occupied) {
            seat.classList.add("occupied");
            seat.classList.remove("free");
        } else {
            seat.classList.add("free");
            seat.classList.remove("occupied");
        }
    }
}

// ---------------- NOISE COLOR ----------------
function updateNoise(level) {
    const box = document.getElementById("noiseBox");

    if (level === "Low") box.style.background = "green";
    else if (level === "Medium") box.style.background = "orange";
    else box.style.background = "red";

    box.innerText = "Noise: " + level;
}

// ---------------- CREATE CHART ----------------
function createChart() {
    const ctx = document.getElementById("chart");

    chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Occupancy %",
                data: dataPoints
            }]
        }
    });
}

// ---------------- FETCH DATA ----------------
async function fetchData() {
    try {
        const res = await fetch(API + "/api/latest");
        if (!res.ok) return;

        const data = await res.json();
        if (!data.occupied_seats) return;

        document.getElementById("stats").innerText =
            `Seats: ${data.occupied_seats}/${data.total_seats}`;

        document.getElementById("prediction").innerText =
            `Predicted Crowd: ${data.predicted_crowd}`;

        updateSeats(data.occupied_seats);
        updateNoise(data.noise_level);

        // Update chart
        labels.push(new Date().toLocaleTimeString());
        dataPoints.push(data.occupancy_percentage);

        if (labels.length > 10) {
            labels.shift();
            dataPoints.shift();
        }

        chart.update();

    } catch (err) {
        console.log("Server error");
    }
}

// ---------------- INIT ----------------
createSeats();
createChart();

// fetch every 5 sec
setInterval(fetchData, 5000);