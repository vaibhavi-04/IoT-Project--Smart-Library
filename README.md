# 📚 Smart Library – IoT + AI Digital Twin

A smart system that monitors library seat occupancy, predicts crowd levels using AI, and displays a live Digital Twin dashboard.

🚀 What It Does

Real-time seat availability

Noise level monitoring

AI-based crowd prediction (Low / Medium / High)

Live seating layout visualization

Occupancy trend graph

🏗️ Architecture
Sensors / Simulator
        ↓
ESP32 (Edge – simulated)
        ↓
Flask Backend (Cloud API)
        ↓
AI Model (Crowd Prediction)
        ↓
Web Dashboard (Digital Twin + Analytics)
🛠️ Tech Stack

ESP32 (planned hardware)

Flask (backend API)

scikit-learn (AI model)

Chart.js (dashboard graphs)

HTML / CSS / JavaScript

⚙️ Quick Start
pip install flask flask-cors scikit-learn numpy requests
# Train AI model
cd ai
python train_model.py

# Run backend
cd ../backend
python server.py

# Run simulator
cd ../simulator
python fake_data.py

# Run dashboard
cd ../dashboard
python -m http.server 8000

Open: http://127.0.0.1:8000

📌 Status

✔ End-to-end working (simulated sensors)
✔ AI integrated with live API
✔ Digital Twin dashboard operational
✔ Real-time graph updates

Hardware deployment pending.

🎯 Goal

To help students decide when and where to study using real-time IoT data and predictive analytics.
