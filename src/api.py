from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException

from src.anomaly_detection import detect_anomalies

app = FastAPI(
    title="Financial Transaction Anomaly Detection API",
    version="1.0.0",
)

RESULTS_PATH = Path("results/anomaly_predictions.csv")


@app.get("/")
def home():
    return {
        "message": "Anomaly Detection API is running",
        "status": "healthy",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/detect-anomalies")
def run_anomaly_detection():
    try:
        detect_anomalies()

        df = pd.read_csv(RESULTS_PATH)
        anomalies = df[df["predicted_anomaly"] == 1]

        return {
            "status": "success",
            "total_transactions": int(len(df)),
            "detected_anomalies": int(len(anomalies)),
            "anomalies": anomalies[
                [
                    "transaction_id",
                    "amount",
                    "hour",
                    "anomaly_score",
                ]
            ].to_dict(orient="records"),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Anomaly detection failed. Check API logs.",
        ) from exc


@app.get("/validate-data")
def validate_data():
    """Validate financial transaction data before anomaly detection."""
    try:
        import pandas as pd
        from src.data_quality import validate_transactions

        df = pd.read_csv("data/transactions.csv")
        return validate_transactions(df)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Data validation failed: {exc}"
        )
