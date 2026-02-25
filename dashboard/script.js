let chart;
let labels = [];
let occupancyData = [];
const totalSeats = 10;
const API_URL = "http://127.0.0.1:5000/api/latest";

function createChart() {
    const ctx = document.getElementById("occupancyChart").getContext("2d");

    chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Occupancy %",
                data: occupancyData,
                borderColor: "blue",
                fill: false
            }]
        },
        options: {
            scales: {
                y: {
                    min: 0,
                    max: 100
                }
            }
        }
    });
}

function createSeats() {
    const container = document.getElementById("seats");
    container.innerHTML = "";

    for (let i = 0; i < totalSeats; i++) {
        const seat = document.createElement("div");
        seat.className = "seat free";
        seat.id = "seat-" + i;
        container.appendChild(seat);
    }
}

async function fetchData() {
    const res = await fetch(API_URL);
    const data = await res.json();

    if (data.occupied_seats === undefined) return;

    document.getElementById("stats").innerHTML =
        "Occupied Seats: " + data.occupied_seats +
        " / " + data.total_seats;

    document.getElementById("noise").innerHTML =
        "Noise Level: " + data.noise_level +
        " | Predicted Crowd: " + data.predicted_crowd;

    updateSeats(data.occupied_seats);

    // --------- Graph Update Logic ----------
    const now = new Date().toLocaleTimeString();

    labels.push(now);
    occupancyData.push(data.occupancy_percentage);

    if (labels.length > 10) {
        labels.shift();
        occupancyData.shift();
    }

    chart.update();
}

function updateSeats(occupied) {
    for (let i = 0; i < totalSeats; i++) {
        const seat = document.getElementById("seat-" + i);
        seat.className = i < occupied ? "seat occupied" : "seat free";
    }
}



createSeats();
createChart();
setInterval(fetchData, 5000);