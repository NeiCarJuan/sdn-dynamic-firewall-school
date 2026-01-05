import json
from features import extract_features

MODEL_FILE = "model_state.json"

def load_model():
    with open(MODEL_FILE, "r") as f:
        return json.load(f)

def save_model(model):
    with open(MODEL_FILE, "w") as f:
        json.dump(model, f, indent=2)

def compute_score(features):
    return (
        0.4 * features["ping_rate"] +
        0.3 * features["burstiness"] +
        0.3 * features["dst_variance"]
    )

def detect_anomaly(event_counter):
    model = load_model()
    features = extract_features(event_counter)
    score = compute_score(features)

    model["history"].append(score)

    if score > model["threshold"]:
        model["threshold"] += 1.0   # adaptive learning
        save_model(model)
        return True, score

    save_model(model)
    return False, score

