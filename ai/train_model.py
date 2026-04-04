import pickle
from sklearn.ensemble import RandomForestClassifier
from prepare_data import X, y

model = RandomForestClassifier()
model.fit(X, y)

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained using Wokwi data")