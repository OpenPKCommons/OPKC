"""
Hakki et al. 2022 (DOI: 10.1016/S2213-2600(22)00226-0)
========================================================
Study summary:
---------------
This study followed household contacts of confirmed COVID-19 cases with 
daily upper respiratory tract (URT) sampling for up to 20 days after exposure. 
Both viral RNA load (by RT-qPCR) and infectious virus (by plaque assay, PFU/mL) 
were quantified longitudinally for each participant.

Temporal variables:
-------------------
- `day` represents the number of days since the **first PCR-positive sample** 
  for each participant. This is mapped to the schema variable `TimeDays`.

- `days_since_peak` represents days relative to the **peak viral RNA load** 
  (per participant). Negative values indicate days before the peak, positive 
  values indicate days after the peak. This field is retained as 
  `DaysSincePeak` for optional use in modeling viral trajectory alignment.

Data source:
------------
Raw dataset: trajectories.csv, available from the authors’ GitHub repository:
https://github.com/HPRURespMed/SARS-CoV-2-viral-shedding-dynamics/tree/main/Data

Notes:
------
- Viral load (`copy`) and infectious titre (`pfu`) were reported in units per mL.
- `Log10VL` is computed from these raw values (non-positive values → NaN).
- Default assumptions: SampleType = "combined_nose_throat_swab", Platform = "RT-qPCR"
  (update if further methodological details confirm otherwise).
  - Sampling involved combined nose-and-throat (URT) swabs, treated as "combined_nose_throat_swab"
  for schema consistency across datasets.
"""

import math
import pandas as pd
# Make parent folder importable to import schema.py
import os, sys
THIS_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.abspath(os.path.join(THIS_DIR, ".."))  # .../ingest_studies
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)
from schema import enforce_schema, coerce_types  # split_age_range if needed

def _safe_log10(x):
    """Return log10(x) for positive x, else NaN."""
    try:
        x = float(x)
        return math.log10(x) if x > 0 else float("nan")
    except Exception:
        return float("nan")

def load_and_format():
    # 1) Load Hakki raw CSV placed at: data/hakki2022.csv
    # Construct path relative to this script — portable across machines
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    csv_path = os.path.join(base_dir, "data", "hakki2022.csv")
    df = pd.read_csv(csv_path)

    # 2) Keep only the columns needed (defensive: keep only those that exist)
    raw_cols = [
        "participant",       # subject id
        "day",               # a time variable (see NOTE below)
        "days_since_peak",   # alt time ref; keep as extra metadata
        "copy",              # genome copies per mL (numeric)
        "pfu",               # PFU per mL (numeric)
        "LFD",               # lateral flow result (binary/boolean-ish)
        "vaccinated",        # vaccination status (binary/str)
        "WGS"                # lineage/variant label (e.g., "Pre-Alpha")
    ]
    keep = [c for c in raw_cols if c in df.columns]
    df = df[keep].copy()

    # 3) Rename to the lab schema names used elsewhere
    # If future data revisions rename 'day' to something else (e.g., 'days_post_exposure'),
    # update this map accordingly to preserve the TimeDays variable definition.

    rename_map = {
        "participant": "PersonID",
        "day": "TimeDays",
        "days_since_peak": "DaysSincePeak",
        "copy": "CopiesPerML",
        "pfu": "PFUPerML",
        "LFD": "LFD_Positive",
        "vaccinated": "Vaccinated",
        "WGS": "Subtype"
    }
    present_map = {k: v for k, v in rename_map.items() if k in df.columns}
    df = df.rename(columns=present_map)

    # 4) Coerce some types
    for c in ["CopiesPerML", "PFUPerML", "TimeDays", "DaysSincePeak"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # 5) Build the measurement column expected by lab schema
    # Russell2024 used Log10VL + Units. Prefer quantitative load if available:
    #   - If CopiesPerML present: Log10VL = log10(copies/mL), Units = "log10(copies/mL)"
    #   - Else if PFUPerML present: Log10VL = log10(PFU/mL), Units = "log10(PFU/mL)"
    #   - Else (no quantitative): keep Units as "Ct" only if you map Ct elsewhere (not present here); otherwise leave NA.
    if "CopiesPerML" in df.columns and df["CopiesPerML"].notna().any():
        df["Log10VL"] = df["CopiesPerML"].apply(_safe_log10)
        df["Units"] = "log10(copies/mL)"
    elif "PFUPerML" in df.columns and df["PFUPerML"].notna().any():
        df["Log10VL"] = df["PFUPerML"].apply(_safe_log10)
        df["Units"] = "log10(PFU/mL)"
    else:
        # No quantitative load; leave Log10VL as NaN and Units unspecified.
        df["Log10VL"] = float("nan")
        df["Units"] = pd.NA

    # 6) Fill study-level metadata lab schema expects
    df["StudyID"] = "hakki2022"
    df["Pathogen"] = "SARS2"
    df["PtSpecies"] = "Human"
    df["DOI"] = "10.1016/S2213-2600(22)00226-0"
    # SampleType/Platform - set conservative defaults; refine from Methods later if needed
    if "SampleType" not in df.columns:
        df["SampleType"] = "combined_nose_throat_swab"
    if "Platform" not in df.columns:
        df["Platform"] = "RT-qPCR"           # TODO: refine targets if I extract them later

    # Optional: normalize booleans
    if "LFD_Positive" in df.columns:
        df["LFD_Positive"] = df["LFD_Positive"].map({1: True, 0: False, "1": True, "0": False}).fillna(df["LFD_Positive"])

    # 7) Enforce schema and types
    df = enforce_schema(df)
    df = coerce_types(df)

    # Keep DaysSincePeak as an extra variable if lab schema allows unknowns; else drop it
    # If enforce_schema drops unknown columns, store in a Notes column.
    print(f"Loaded Hakki et al. 2022 — {len(df)} total rows.")
    return df
if __name__ == "__main__":
    df = load_and_format()
    print(f"Loaded from: {__file__}")
    print(df.shape)
    print(df.columns.tolist())
    print(df.head().to_string(index=False))
