import pickle
import numpy as np
import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ✅ DEFINE DATA FILE
DATA_FILE = "data.json"

# Ensure file exists
if not os.path.exists(DATA_FILE):
    open(DATA_FILE, "w").close()

# Load AI model
with open("../ai/model.pkl", "rb") as f:
    model = pickle.load(f)

latest_data = {}
history = []

# ---------------- POST ----------------
@app.route("/api/data", methods=["POST"])
def receive_data():
    global latest_data, history

    data = request.json
    print("Received:", data)

    data["timestamp"] = datetime.now().isoformat()

    latest_data = data

    history.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "occupancy": data["occupancy_percentage"]
    })

    # ✅ FIXED FILE WRITE
    with open(DATA_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")

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

    now = datetime.now()

    features = np.array([[
        now.hour,
        now.weekday(),
        latest.get("occupancy_percentage", 0)
    ]])

    pred = model.predict(features)[0]

    # ✅ FIX BASED ON MODEL TYPE

    # If using OLD model (3 classes)
    # label_map = {0: "Low", 1: "Medium", 2: "High"}

    # If using NEW next-hour model (binary)
    label_map = {
        0: "Not High (Next Hour)",
        1: "High (Next Hour)"
    }

    latest["predicted_crowd"] = label_map[pred]

    return jsonify(latest)


# ---------------- GET HISTORY ----------------
@app.route("/api/history", methods=["GET"])
def get_history():
    return jsonify(history)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)