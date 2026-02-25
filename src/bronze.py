"""Bronze layer: raw ingestion with no transformations."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


DATA_FILES = {
    "ehr": ["ehr.csv"],
    "vitals": ["vitals.csv", "vitals.jsonl"],
    "labs": ["labs.csv", "labs.json"],
}


def _find_source_file(data_dir: Path, candidates: list[str]) -> Path:
    for candidate in candidates:
        candidate_path = data_dir / candidate
        if candidate_path.exists():
            return candidate_path
    raise FileNotFoundError(f"None of the expected source files were found: {candidates}")


def _read_to_dataframe(file_path: Path) -> pd.DataFrame:
    suffix = file_path.suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(file_path)

    if suffix == ".jsonl":
        records = [json.loads(line) for line in file_path.read_text().splitlines() if line.strip()]
        return pd.DataFrame(records)

    if suffix == ".json":
        loaded = json.loads(file_path.read_text())
        if isinstance(loaded, list):
            return pd.DataFrame(loaded)
        raise ValueError(f"JSON source file must contain a list of records: {file_path}")

    raise ValueError(f"Unsupported source format: {file_path}")


def run_bronze_layer(data_dir: Path, bronze_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Ingest source files and store raw copies as CSV in bronze."""
    ehr_source = _find_source_file(data_dir, DATA_FILES["ehr"])
    vitals_source = _find_source_file(data_dir, DATA_FILES["vitals"])
    labs_source = _find_source_file(data_dir, DATA_FILES["labs"])

    ehr_df = _read_to_dataframe(ehr_source)
    vitals_df = _read_to_dataframe(vitals_source)
    labs_df = _read_to_dataframe(labs_source)

    ehr_df.to_csv(bronze_dir / "ehr.csv", index=False)
    vitals_df.to_csv(bronze_dir / "vitals.csv", index=False)
    labs_df.to_csv(bronze_dir / "labs.csv", index=False)

    return ehr_df, vitals_df, labs_df
