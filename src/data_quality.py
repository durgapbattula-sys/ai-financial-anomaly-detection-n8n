import json
from pathlib import Path

import pandas as pd

DATA_PATH = Path("data/transactions.csv")
REPORT_PATH = Path("results/data_quality_report.json")

REQUIRED_COLUMNS = [
    "transaction_id",
    "amount",
    "hour",
]


def validate_transactions(df):
    issues = {}

    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    issues["missing_columns"] = missing_columns

    if missing_columns:
        return {
            "status": "failed",
            "total_records": len(df),
            "issues": issues,
        }

    transaction_ids = df["transaction_id"].astype("string")

    missing_ids = (
        transaction_ids.isna()
        | transaction_ids.str.strip().eq("").fillna(False)
    )

    amounts = pd.to_numeric(df["amount"], errors="coerce")
    hours = pd.to_numeric(df["hour"], errors="coerce")

    issues["missing_transaction_ids"] = int(missing_ids.sum())

    issues["duplicate_transaction_ids"] = int(
        df.loc[~missing_ids, "transaction_id"]
        .duplicated()
        .sum()
    )

    issues["invalid_amounts"] = int(
        (amounts.isna() | (amounts < 0)).sum()
    )

    issues["invalid_hours"] = int(
        (
            hours.isna()
            | (hours < 0)
            | (hours > 23)
            | (hours % 1 != 0)
        ).sum()
    )

    total_issues = sum(
        value for value in issues.values()
        if isinstance(value, int)
    )

    return {
        "status": "passed" if total_issues == 0 else "failed",
        "total_records": len(df),
        "total_issues": total_issues,
        "issues": issues,
    }


def main():
    df = pd.read_csv(DATA_PATH)

    report = validate_transactions(df)

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT_PATH.write_text(
        json.dumps(report, indent=2)
    )

    print(json.dumps(report, indent=2))
    print(f"Report saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
