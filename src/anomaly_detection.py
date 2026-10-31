from pathlib import Path

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
)

DATA_PATH = Path("data/transactions.csv")
RESULTS_PATH = Path("results/anomaly_predictions.csv")


def detect_anomalies():
    df = pd.read_csv(DATA_PATH)

    # Select only the features used by the model.
    features = df[["amount", "hour"]]

    # Train an unsupervised anomaly detection model.
    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42,
    )

    predictions = model.fit_predict(features)

    # Isolation Forest returns -1 for anomalies and 1 for normal.
    df["predicted_anomaly"] = (
        predictions == -1
    ).astype(int)

    df["anomaly_score"] = (
        -model.decision_function(features)
    )

    # Evaluate against synthetic labels.
    actual = df["is_synthetic_anomaly"]
    predicted = df["predicted_anomaly"]

    print("Isolation Forest Results")
    print("------------------------")
    print(f"Total transactions: {len(df)}")
    print(f"Detected anomalies: {predicted.sum()}")
    print(f"Precision: {precision_score(actual, predicted):.3f}")
    print(f"Recall: {recall_score(actual, predicted):.3f}")
    print(f"F1 Score: {f1_score(actual, predicted):.3f}")

    RESULTS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(RESULTS_PATH, index=False)
    print(f"Results saved to: {RESULTS_PATH}")


if __name__ == "__main__":
    detect_anomalies()
