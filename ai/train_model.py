import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle

# Training Data Format:
# [hour_of_day, day_of_week, occupancy_percent]

X = [
    [9, 1, 20],
    [10, 1, 40],
    [11, 1, 70],
    [15, 3, 85],
    [18, 5, 90],
    [8, 6, 30],
    [13, 2, 60],
    [16, 4, 75]
]

# Labels:
# 0 = Low
# 1 = Medium
# 2 = High
y = [0, 1, 2, 2, 2, 0, 1, 2]

model = RandomForestClassifier()
model.fit(X, y)

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved successfully")