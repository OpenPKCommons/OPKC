"""
Test one study's ingestion in isolation. Handy for iterating on a single
study without regenerating the full combined dataset.

Usage (from anywhere):
    python3 code/ingest_studies/test_import.py <study_name>

Example:
    python3 code/ingest_studies/test_import.py facciuolo2025

Writes: output/test_import.csv
"""
import argparse
import importlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = REPO_ROOT / "output" / "test_import.csv"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "study_name",
        help="Module in studies/ (e.g. 'facciuolo2025')",
    )
    args = parser.parse_args()

    module = importlib.import_module(f"studies.{args.study_name}")
    df = module.load_and_format()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    populated = [c for c in df.columns if df[c].notna().any()]
    print(f"Wrote {len(df):,} rows from {args.study_name} to {OUTPUT_PATH}")
    print(f"Populated columns ({len(populated)}/{len(df.columns)}): {populated}")


if __name__ == "__main__":
    main()
