import numpy as np
import pandas as pd
from pathlib import Path

OUTPUT_PATH = Path("data/transactions.csv")
RANDOM_SEED = 42


def generate_transactions():
    rng = np.random.default_rng(RANDOM_SEED)

    normal_count = 950
    anomaly_count = 50

    # Generate normal transactions
    normal_amounts = rng.lognormal(
        mean=4.0,
        sigma=0.7,
        size=normal_count
    )

    # Generate unusually large transactions
    anomaly_amounts = rng.uniform(
        low=3000,
        high=15000,
        size=anomaly_count
    )

    amounts = np.concatenate([
        normal_amounts,
        anomaly_amounts
    ])

    hours = np.concatenate([
        rng.integers(7, 23, normal_count),
        rng.integers(0, 5, anomaly_count)
    ])

    transaction_types = rng.choice(
        ["purchase", "transfer", "withdrawal"],
        size=normal_count + anomaly_count
    )

    labels = np.concatenate([
        np.zeros(normal_count, dtype=int),
        np.ones(anomaly_count, dtype=int)
    ])

    df = pd.DataFrame({
        "transaction_id": [
            f"TXN{i:06d}"
            for i in range(1, 1001)
        ],
        "amount": np.round(amounts, 2),
        "hour": hours,
        "transaction_type": transaction_types,
        "is_synthetic_anomaly": labels
    })

    # Shuffle transactions
    df = df.sample(
        frac=1,
        random_state=RANDOM_SEED
    ).reset_index(drop=True)

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(OUTPUT_PATH, index=False)

    print("Dataset generated successfully!")
    print(f"Total transactions: {len(df)}")
    print(
        "Injected anomalies:",
        df["is_synthetic_anomaly"].sum()
    )
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_transactions()
