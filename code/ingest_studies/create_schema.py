"""
Build the combined viral-kinetics dataset from all ingested studies.

Usage (from anywhere; paths resolve relative to this file):
    python3 code/ingest_studies/create_schema.py

Writes: output/combined_cleaned_data_staged.csv

To publish the staged CSV to the website, copy it to
output/combined_cleaned_data_published.csv. See output/README.md for the
staged-vs-published workflow.
"""
import importlib
from pathlib import Path

import pandas as pd

# Studies included in the combined dataset (alpha order). To add a new one, drop
# a module in studies/ exposing load_and_format() and add its module name below.
STUDIES = [
    "alahakoon2025",
    "eales2025",
    "facciuolo2025",
    "hakki2022",
    "jones2021",
    "ke2022",
    "kissler2023",
    # "Kucirka2020",    # excluded — ingest not currently wired in
    "penamosca2025",
    "puhach2022",
    "russell2024",
    "savela2022",
    # "vanKampen2021",  # excluded — ingest not currently wired in
    "vuong2024",
    "wagstaffe2024",
    "waickman2022",
    "waickman2024",
    "wongnak2024",
]

# Repo root = three levels up from this file. Using an absolute path means the
# script works regardless of the caller's working directory.
REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = REPO_ROOT / "output" / "combined_cleaned_data_staged.csv"


def _assign_global_ids(df):
    """Populate GlobalIndivID, GlobalInfectionID, GlobalSampleID.

    Studies use their own ID schemes for people, infections, and samples, which
    can collide across studies (e.g. two different studies both label a patient
    "1"). We add three dataset-wide unique columns while preserving the original
    per-study IDs alongside them for back-tracing.

    - GlobalIndivID:     "<StudyID>_<IndivID>" when IndivID is set, else NA.
    - GlobalSampleID:    "<StudyID>_<SampleID>" when SampleID is set, else NA.
    - GlobalInfectionID: per person, a running 1..n index over their distinct
      study-supplied InfectionID values, ordered by first appearance. A person
      with no InfectionID at all counts as contributing a single infection (=1).
    """
    # coerce_types runs per-study before concat and str-casts string columns, so
    # real nulls in IndivID / InfectionID / SampleID arrive here as the literal
    # string "<NA>" (or occasionally "nan"). Treat all three forms as null.
    def _is_null(s):
        return s.isna() | s.astype(str).isin(["<NA>", "nan", "NaN"])

    # GlobalIndivID: <StudyID>_<IndivID>
    df["GlobalIndivID"] = pd.NA
    mask = ~_is_null(df["IndivID"]) & ~_is_null(df["StudyID"])
    df.loc[mask, "GlobalIndivID"] = (
        df.loc[mask, "StudyID"].astype(str) + "_" + df.loc[mask, "IndivID"].astype(str)
    )

    # GlobalSampleID: <StudyID>_<SampleID>
    df["GlobalSampleID"] = pd.NA
    mask = ~_is_null(df["SampleID"]) & ~_is_null(df["StudyID"])
    df.loc[mask, "GlobalSampleID"] = (
        df.loc[mask, "StudyID"].astype(str) + "_" + df.loc[mask, "SampleID"].astype(str)
    )

    # GlobalInfectionID: within each person, factorize their distinct raw
    # InfectionID values (nulls collapse to a single implicit infection = 1).
    inf_key = df["InfectionID"].where(~_is_null(df["InfectionID"]), other="__none__")
    df["GlobalInfectionID"] = pd.NA
    mask = df["GlobalIndivID"].notna()
    df.loc[mask, "GlobalInfectionID"] = (
        df.loc[mask]
          .assign(_k=inf_key.loc[mask])
          .groupby("GlobalIndivID", sort=False)["_k"]
          .transform(lambda s: pd.factorize(s, sort=False)[0] + 1)
    )


def main():
    frames = []
    for name in STUDIES:
        module = importlib.import_module(f"studies.{name}")
        frames.append(module.load_and_format())
    combined_df = pd.concat(frames, ignore_index=True)
    _assign_global_ids(combined_df)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    combined_df.to_csv(OUTPUT_PATH, index=False)
    print(f"Wrote {len(combined_df):,} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
