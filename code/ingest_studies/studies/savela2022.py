"""
Savela et al. 2022 (DOI: 10.1128/JCM.01785-21)
====================================================================
Study summary:
---------------
This study followed participants in a household transmission cohort, 
collecting self-administered paired saliva and anterior nares (nasal) swabs 
daily to compare SARS-CoV-2 viral load dynamics between sample types. 
Longitudinal RT-qPCR measurements of N1 and N2 gene targets were used to 
quantify viral load (copies/mL) and assess diagnostic sensitivity by sample 
type and time since infection onset.

Temporal variables:
-------------------
- `Days Post-Enrollment` represents the number of days since **study enrollment** 
  for each participant. We re-baseline per person so that the **first detectable**
  sample (i.e., first non-ND) is set to TimeDays = 0.0.

- Additional time variables in some supplemental files (e.g., `days_4C`, 
  `day_archive`) reflect storage or extraction stability experiments rather than 
  within-host infection progression, and are therefore retained only in 
  `savela2022_swab_SI` and `savela2022_saliva_SI`–derived tables.

Data source:
------------
Raw datasets downloaded from the CaltechDATA repository:
https://data.caltech.edu/records/20047

Files used:
------------
- savela2022_fig2A_paired.xlsx through savela2022_fig2G_paired.xlsx
- savela2022_saliva.xlsx
- savela2022_saliva_SI.xlsx
- savela2022_swab.xlsx
- savela2022_swab_SI.csv
- savela2022_Data_Annotation.pdf (metadata reference)

Notes:
------
- Sample types include paired saliva and anterior nares (AN) swabs; no 
  nasopharyngeal samples were collected.
- Viral load values (`Viral Load N1`/`N2`) reported as copies per mL.
- `Log10VL` computed as log10 of the mean viral load across N1 and N2 targets.
- Self-collected samples; household study conducted during the early 2022 
  Omicron transmission period.
- Data aggregated across multiple figure-level files into a unified schema via 
  `load_and_format()`.
"""

import os, sys, math
import pandas as pd
import numpy as np
# Make parent folder importable to import schema.py
THIS_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.abspath(os.path.join(THIS_DIR, ".."))  # .../ingest_studies
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from schema import enforce_schema, coerce_types

def _sample_fields_from_text(txt: str):
    """
    Map raw 'Sample Type' text into (SampleSource, SampleMethod).
    Expected sample_type_str contains something like 'saliva' or 'nasal swab'.
    """
    if not isinstance(txt, str):
        return (pd.NA, pd.NA)
    t = txt.strip().lower()
    if "saliva" in t:
        return ("saliva", "saliva collection")
    # Savela uses anterior nares (nasal) swabs
    if "nasal" in t or "nares" in t or "anterior" in t or "swab" in t:
        return ("anterior nares", "swab")
    return (pd.NA, pd.NA)

def _safe_log10(x):
    """Return log10(x) for positive x, else NaN."""
    try:
        x = float(x)
        return math.log10(x) if x > 0 else float("nan")
    except Exception:
        return float("nan")


def load_savela2022_infection(data_dir: str) -> pd.DataFrame:
    """Load and standardize longitudinal infection data (Fig 2A–G paired)."""
    infection_files = sorted(
        f for f in os.listdir(data_dir)
        if f.startswith("savela2022_fig2") and f.endswith(".xlsx")
    )
    if not infection_files:
        raise FileNotFoundError("No savela2022_fig2*.xlsx files found in data directory.")

    frames = []
    age_map = {
        "A": (30, 39),
        "B": (50, 59),
        "C": (50, 59),
        "D": (12, 17), # No raw data for Fig 2D in CaltechDATA repository
        "E": (30, 39), # No raw data for Fig 2E in CaltechDATA repository
        "F": (6, 11), # No raw data for Fig 2F in CaltechDATA repository
        "G": (50, 59),
    }    
    for f in infection_files:
        raw = pd.read_excel(os.path.join(data_dir, f))

        # Clean and standardize
        df = raw.rename(columns={
            "Participant": "IndivID",
            "Days Post-Enrollment": "TimeDays",
            "Viral Load N1 (copies/mL)": "Target1", # will copy below to PathogenLoad
            "Viral Load N2 (copies/mL)": "Target2", # will copy below to PathogenLoad
        })

        # Parse Sample Type
        ss = df.get("Sample Type")
        sample_pairs = ss.apply(_sample_fields_from_text) if ss is not None else [(pd.NA, pd.NA)] * len(df)
        df["SampleSource"] = [p[0] for p in sample_pairs]
        df["SampleMethod"] = [p[1] for p in sample_pairs]

        # Metadata
        df["StudyID"] = "savela2022"
        df["Pathogen"] = "SARS-CoV-2"
        df["IndivSpecies"] = "Human"
        df["Units"] = "copies/mL"
        df["AssayType"] = "RT-qPCR"
        df["ReadoutPlatform"] = "Bio-Rad CFX96"
        df["DOI"] = "10.1128/JCM.01785-21"

        # Set age ranges based on figure letter
        fig_letter = f.split("fig2")[1][0].upper()
        df["AgeRng1"], df["AgeRng2"] = age_map.get(fig_letter, (pd.NA, pd.NA))

        # Ensure numeric targets
        for col in ["Target1", "Target2"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # N1 rows
        df_n1 = df.copy(deep=True)
        df_n1["AssayTargets"] = "N1"
        df_n1["BiomarkerQuantity"] = df_n1["Target1"].apply(
            lambda x: math.log10(x) if pd.notna(x) and x > 0 else np.nan
        )

        # N2 rows
        df_n2 = df.copy(deep=True)
        df_n2["AssayTargets"] = "N2"
        df_n2["BiomarkerQuantity"] = df_n2["Target2"].apply(
            lambda x: math.log10(x) if pd.notna(x) and x > 0 else np.nan
        )

        use_cols = [
            "StudyID", "IndivID", "Pathogen", "IndivSpecies", "TimeDays",
            "SampleSource", "SampleMethod", "AgeRng1", "AgeRng2", "AssayType", "ReadoutPlatform", "DOI",
            "AssayTargets", "BiomarkerQuantity", "Units"
        ]

        frames.append(df_n1[use_cols])
        frames.append(df_n2[use_cols])

    # Combine everything AFTER the loop
    out = pd.concat(frames, ignore_index=True)

    # Re-baseline TimeDays
    def first_detected_day(g):
        mask = g["BiomarkerQuantity"].notna() & g["TimeDays"].notna()
        if mask.any():
            return g.loc[mask, "TimeDays"].min()
        return np.nan

    shifts = out.groupby("IndivID", dropna=False).apply(first_detected_day, include_groups=False).rename("t0")
    out = out.merge(shifts, on="IndivID", how="left")
    out["TimeDays"] = pd.to_numeric(out["TimeDays"], errors="coerce") - pd.to_numeric(out["t0"], errors="coerce")
    out.drop(columns=["t0"], inplace=True)

    # Final schema alignment
    out["Biomarker"] = "pathogen load"
    out = enforce_schema(out)
    out = coerce_types(out)

    return out


def load_and_format(base_dir=None):
    """
    Master loader for Savela et al. 2022 (version 1 schema-compliant).
    Currently loads only the infection trajectory data (Fig 2A–G paired datasets).
    """
    if base_dir is None:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))

    data_dir = os.path.join(base_dir, "data")
    df_infection = load_savela2022_infection(data_dir)
    #print(f"Loaded Savela et al. 2022 — {len(df_infection)} total rows.")
    return df_infection

"""
# Test block
if __name__ == "__main__":
    df = load_and_format()
    print(df.head(15))
"""