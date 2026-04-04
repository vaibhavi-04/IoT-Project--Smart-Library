import json
from datetime import datetime

data = []

with open("../backend/data.json", "r") as f:
    for line in f:
        data.append(json.loads(line))

X = []
y = []

for i in range(len(data) - 1):
    current = data[i]
    next_data = data[i + 1]

    # Current features
    time_obj = datetime.fromisoformat(current["timestamp"])
    hour = time_obj.hour
    day = time_obj.weekday()
    occupancy = current["occupancy_percentage"]

    # Next hour label
    next_occupancy = next_data["occupancy_percentage"]

    label = 1 if next_occupancy > 70 else 0

    X.append([hour, day, occupancy])
    y.append(label)

print("Samples:", len(X))