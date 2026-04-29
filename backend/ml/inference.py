import joblib
import os

MODEL_PATH = "ml/models/fraud_model.pkl"

model = joblib.load(MODEL_PATH)


def predict_fraud_probability(features):
    row = [[
        features.get("accounts_per_ip", 0),
        features.get("accounts_per_device", 0),
        features.get("accounts_per_user", 0),
        features.get("is_suspicious_ip", 0),
        features.get("is_disposable_email", 0),
        features.get("time_to_submit", 0),
        features.get("keystrokes", 0),
        features.get("mouse_distance", 0)
    ]]

    prob = model.predict_proba(row)[0][1]

    return float(prob)