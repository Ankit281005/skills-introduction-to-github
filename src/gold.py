"""Gold layer: anomaly detection."""

from __future__ import annotations

import pandas as pd


def run_gold_layer(patient_master_df: pd.DataFrame, gold_dir) -> pd.DataFrame:
    """Detect anomalies and save gold output."""
    anomalies = patient_master_df[["patient_id"]].copy()
    anomalies["high_heart_rate"] = patient_master_df["hr"] > 120
    anomalies["low_oxygen"] = patient_master_df["ox"] < 92
    anomalies["high_blood_pressure"] = (patient_master_df["sys"] > 160) | (
        patient_master_df["dia"] > 100
    )

    anomalies.to_csv(gold_dir / "anomalies.csv", index=False)
    return anomalies
