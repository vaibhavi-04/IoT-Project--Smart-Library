import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle

# ---------------- CREATE DATA ----------------

data = []

for day in range(7):
    for hour in range(24):

        # Simulate realistic occupancy
        if 8 <= hour <= 12:
            occupancy = np.random.randint(30, 60)
        elif 12 < hour <= 17:
            occupancy = np.random.randint(60, 90)
        elif 17 < hour <= 21:
            occupancy = np.random.randint(50, 80)
        else:
            occupancy = np.random.randint(5, 30)

        # Add noise factor
        noise = np.random.randint(-10, 10)
        occupancy = max(0, min(100, occupancy + noise))

        # Label
        if occupancy < 40:
            label = 0   # Low
        elif occupancy < 70:
            label = 1   # Medium
        else:
            label = 2   # High

        data.append([hour, day, occupancy, label])

df = pd.DataFrame(data, columns=["hour", "weekday", "occupancy", "label"])

# ---------------- TRAIN MODEL ----------------

X = df[["hour", "weekday", "occupancy"]]
y = df["label"]

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# ---------------- SAVE MODEL ----------------

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained successfully!")