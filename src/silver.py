"""Silver layer: cleaning, standardization, and patient master creation."""

from __future__ import annotations

import pandas as pd


VITAL_NUMERIC_COLUMNS = ["hr", "ox", "sys", "dia"]


def clean_vitals(vitals_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Clean vitals and derive the latest vitals record per patient."""
    cleaned = vitals_df.rename(columns={"patientId": "patient_id"}).copy()

    cleaned["timestamp"] = pd.to_datetime(cleaned["timestamp"], unit="s", errors="coerce")
    for col in VITAL_NUMERIC_COLUMNS:
        cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")

    cleaned = cleaned.sort_values(["patient_id", "timestamp"])
    latest = cleaned.groupby("patient_id", as_index=False).last()

    return cleaned, latest


def clean_labs(labs_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Clean labs and derive the latest lab record per patient and test."""
    cleaned = labs_df.rename(
        columns={"patientId": "patient_id", "test": "lab_test", "value": "lab_value"}
    ).copy()

    cleaned["timestamp"] = pd.to_datetime(cleaned["timestamp"], unit="s", errors="coerce")
    cleaned["lab_value"] = pd.to_numeric(cleaned["lab_value"], errors="coerce")

    cleaned = cleaned.sort_values(["patient_id", "lab_test", "timestamp"])
    latest = cleaned.groupby(["patient_id", "lab_test"], as_index=False).last()

    return cleaned, latest


def build_patient_master(
    ehr_df: pd.DataFrame,
    latest_vitals_df: pd.DataFrame,
    latest_labs_df: pd.DataFrame,
) -> pd.DataFrame:
    """Combine EHR with latest vitals and pivoted latest lab values."""
    patient_master = ehr_df.merge(latest_vitals_df, on="patient_id", how="left")

    labs_wide = (
        latest_labs_df.pivot(index="patient_id", columns="lab_test", values="lab_value")
        .reset_index()
        .rename_axis(None, axis=1)
    )

    patient_master = patient_master.merge(labs_wide, on="patient_id", how="left")
    return patient_master


def run_silver_layer(
    ehr_df: pd.DataFrame,
    vitals_df: pd.DataFrame,
    labs_df: pd.DataFrame,
    silver_dir,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Run all silver transformations and save outputs."""
    clean_vitals_df, latest_vitals_df = clean_vitals(vitals_df)
    clean_labs_df, latest_labs_df = clean_labs(labs_df)
    patient_master_df = build_patient_master(ehr_df, latest_vitals_df, latest_labs_df)

    clean_vitals_df.to_csv(silver_dir / "clean_vitals.csv", index=False)
    clean_labs_df.to_csv(silver_dir / "clean_labs.csv", index=False)
    patient_master_df.to_csv(silver_dir / "patient_master.csv", index=False)

    return clean_vitals_df, clean_labs_df, patient_master_df
