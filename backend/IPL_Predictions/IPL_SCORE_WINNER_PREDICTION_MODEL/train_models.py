import os
import joblib
import pandas as pd
import numpy as np
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from data_preprocessing import load_data, preprocess_data, prepare_features

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MATCHES_PATH = os.path.join(DATA_DIR, "ipl_2024_matches.csv")
DELIVERIES_PATH = os.path.join(DATA_DIR, "ipl_2024_deliveries.csv")
TEAM_STATS_PATH = os.path.join(DATA_DIR, "teamwise_home_and_away.csv")
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
os.makedirs(SAVED_MODELS_DIR, exist_ok=True)

matches, deliveries, team_stats = load_data(
    MATCHES_PATH, DELIVERIES_PATH, TEAM_STATS_PATH
)

processed_matches = preprocess_data(matches, deliveries, team_stats)

X, y, encoders = prepare_features(processed_matches)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

winner_model = RandomForestClassifier(n_estimators=100, random_state=42)
winner_model.fit(X_train, y_train)

y_pred = winner_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

conf_matrix = confusion_matrix(y_test, y_pred).tolist()
class_report = classification_report(y_test, y_pred, output_dict=True)
feature_importance = pd.DataFrame(
    {"feature": X.columns, "importance": winner_model.feature_importances_}
).sort_values("importance", ascending=False)

output = {
    "accuracy": accuracy,
    "confusion_matrix": conf_matrix,
    "classification_report": class_report,
    "feature_importance": feature_importance.to_dict(orient="records"),
}

output_path = os.path.join(SAVED_MODELS_DIR, "model_evaluation.json")
with open(output_path, "w") as f:
    json.dump(output, f, indent=4)
print(f"Model evaluation saved to {output_path}")

joblib.dump(winner_model, os.path.join(SAVED_MODELS_DIR, "winner_model.pkl"))
joblib.dump(encoders, os.path.join(SAVED_MODELS_DIR, "encoders.pkl"))