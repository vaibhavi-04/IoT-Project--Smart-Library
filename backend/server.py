import pickle
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Load AI model
with open("../ai/model.pkl", "rb") as f:
    model = pickle.load(f)

# In-memory storage (FAST + NO RELOAD)
latest_data = {}
history = []   # for graph

# ---------------- POST (ESP32 → Backend) ----------------
@app.route("/api/data", methods=["POST"])
def receive_data():
    global latest_data, history

    data = request.json
    data["timestamp"] = datetime.now().isoformat()

    # Save latest
    latest_data = data

    # Store for graph
    history.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "occupancy": data["occupancy_percentage"]
    })

    # keep last 20 points
    if len(history) > 20:
        history.pop(0)

    return jsonify({"status": "ok"})


# ---------------- GET LATEST ----------------
@app.route("/api/latest", methods=["GET"])
def get_latest():
    global latest_data

    if not latest_data:
        return jsonify({})

    latest = latest_data.copy()

    # AI Prediction
    now = datetime.now()
    features = np.array([[
        now.hour,
        now.weekday(),
        latest.get("occupancy_percentage", 0)
    ]])

    pred = model.predict(features)[0]
    label_map = {0: "Low", 1: "Medium", 2: "High"}

    latest["predicted_crowd"] = label_map[pred]

    return jsonify(latest)


# ---------------- GET HISTORY (for graph) ----------------
@app.route("/api/history", methods=["GET"])
def get_history():
    return jsonify(history)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)