"""Visualization generation for the hospital data pipeline."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


def _plot_hr_trend(clean_vitals_df: pd.DataFrame, viz_dir) -> None:
    plt.figure(figsize=(10, 6))
    for patient_id, group in clean_vitals_df.groupby("patient_id"):
        plt.plot(group["timestamp"], group["hr"], marker="o", label=f"Patient {patient_id}")

    plt.title("Heart Rate Trend by Patient")
    plt.xlabel("Timestamp")
    plt.ylabel("Heart Rate (bpm)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(viz_dir / "hr_trend.png")
    plt.close()


def _plot_oxygen_distribution(clean_vitals_df: pd.DataFrame, viz_dir) -> None:
    plt.figure(figsize=(8, 5))
    plt.hist(clean_vitals_df["ox"].dropna(), bins=10, edgecolor="black")
    plt.axvline(92, color="red", linestyle="--", linewidth=2, label="Low O2 threshold (92%)")
    plt.title("Oxygen Saturation Distribution")
    plt.xlabel("Oxygen Saturation (%)")
    plt.ylabel("Count")
    plt.legend()
    plt.tight_layout()
    plt.savefig(viz_dir / "oxygen_distribution.png")
    plt.close()


def _plot_anomaly_counts(anomalies_df: pd.DataFrame, viz_dir) -> None:
    counts = anomalies_df[["high_heart_rate", "low_oxygen", "high_blood_pressure"]].sum()

    plt.figure(figsize=(8, 5))
    plt.bar(counts.index, counts.values)
    plt.title("Anomaly Counts")
    plt.xlabel("Anomaly Type")
    plt.ylabel("Number of Patients")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(viz_dir / "anomaly_counts.png")
    plt.close()


def run_visualizations(clean_vitals_df: pd.DataFrame, anomalies_df: pd.DataFrame, viz_dir) -> None:
    """Generate all required visualizations."""
    _plot_hr_trend(clean_vitals_df, viz_dir)
    _plot_oxygen_distribution(clean_vitals_df, viz_dir)
    _plot_anomaly_counts(anomalies_df, viz_dir)
