import pickle
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)

# Load AI model
MODEL_PATH = "../ai/model.pkl"

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)
DATA_FILE = "data.json"

# Ensure data file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        pass


# API to receive sensor data (POST)
@app.route("/api/data", methods=["POST"])
def receive_data():
    data = request.json
    data["timestamp"] = datetime.now().isoformat()

    with open(DATA_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")

    return {"status": "data stored successfully"}


# API to get latest data (GET)
@app.route("/api/latest", methods=["GET"])
def get_latest():
    try:
        with open(DATA_FILE, "r") as f:
            lines = f.readlines()
            if not lines:
                return jsonify({})
            latest = json.loads(lines[-1])

        # Prepare AI features
        now = datetime.now()
        hour = now.hour
        day = now.weekday()
        occupancy = latest["occupancy_percentage"]

        features = np.array([[hour, day, occupancy]])

        prediction = model.predict(features)[0]

        label_map = {
            0: "Low",
            1: "Medium",
            2: "High"
        }

        latest["predicted_crowd"] = label_map[prediction]

        return jsonify(latest)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)