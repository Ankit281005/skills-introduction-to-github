"""Main orchestration script for the hospital data pipeline."""

from __future__ import annotations

from pathlib import Path

from src.bronze import run_bronze_layer
from src.gold import run_gold_layer
from src.silver import run_silver_layer
from src.utils import ensure_directories, log_step
from src.visualize import run_visualizations


def main() -> None:
    project_root = Path(__file__).resolve().parent
    data_dir = project_root / "data"
    bronze_dir = project_root / "bronze"
    silver_dir = project_root / "silver"
    gold_dir = project_root / "gold"
    viz_dir = project_root / "visualizations"

    ensure_directories(project_root)
    log_step("Setup complete: ensured required folders exist")

    ehr_df, vitals_df, labs_df = run_bronze_layer(data_dir, bronze_dir)
    log_step("Bronze layer complete: raw data ingested and copied")

    clean_vitals_df, clean_labs_df, patient_master_df = run_silver_layer(
        ehr_df, vitals_df, labs_df, silver_dir
    )
    log_step("Silver layer complete: data cleaned and patient master built")

    anomalies_df = run_gold_layer(patient_master_df, gold_dir)
    log_step("Gold layer complete: anomalies detected")

    run_visualizations(clean_vitals_df, anomalies_df, viz_dir)
    log_step("Visualization layer complete: charts generated")

    log_step("Pipeline finished successfully")


if __name__ == "__main__":
    main()
