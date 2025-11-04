"""
Savela et al. 2022 (DOI: 10.1126/microbiol.abh2556)
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
    Map raw 'Sample Type' text into (SampleSource1, SampleMethod).
    Expected sample_type_str contains something like 'saliva' or 'nasal swab'.
    """
    if not isinstance(txt, str):
        return (pd.NA, pd.NA)
    t = txt.strip().lower()
    if "saliva" in t:
        return ("saliva", "saliva collection")
    # Savela uses anterior nares (nasal) swabs
    if "nasal" in t or "nares" in t or "anterior" in t or "swab" in t:
        return ("nose", "swab")
    return (pd.NA, pd.NA)

def _safe_log10_mean(n1, n2):
    """
    Compute log10 of mean copies/mL across N1 & N2 if either is valid (>0).
    If both are missing/nonpositive, return NaN.
    """
    vals = [v for v in [n1, n2] if pd.notna(v) and v > 0]
    if not vals:
        return np.nan
    return math.log10(np.mean(vals))


def load_savela2022_infection(data_dir: str) -> pd.DataFrame:
    """Load and standardize longitudinal infection data (Fig 2A–G paired)."""
    infection_files = sorted(
        f for f in os.listdir(data_dir)
        if f.startswith("savela2022_fig2") and f.endswith(".xlsx")
    )
    if not infection_files:
        raise FileNotFoundError("No savela2022_fig2*.xlsx files found in data directory.")

    frames = []
    for f in infection_files:
        raw = pd.read_excel(os.path.join(data_dir, f))
        # Clean and standardize
        df = raw.rename(columns={
            "Participant": "PersonID",
            "Days Post-Enrollment": "TimeDays",
            "Viral Load N1 (copies/mL)": "Target1",
            "Viral Load N2 (copies/mL)": "Target2",
        })
   
# Parse Sample Type into SampleSource1 & SampleMethod
        ss = df.get("Sample Type")
        sample_pairs = ss.apply(_sample_fields_from_text) if ss is not None else [(pd.NA, pd.NA)] * len(df)
        df["SampleSource1"] = [p[0] for p in sample_pairs]
        df["SampleMethod"]  = [p[1] for p in sample_pairs]
#Fixed metadata
    df["StudyID"] = "savela2022"
    df["Pathogen"] = "SARS-CoV-2"
    df["PtSpecies"] = "Human"
    df["Units"] = "copies/mL"
    df["Platform"] = "RT-qPCR"
    df["DOI"] = "10.1126/microbiol.abh2556"
    #df["AgeRng1"] = "6-11"
    #df["AgeRng2"] = "12-17"
    #df["AgeRng3"] = "30-39"
    #df["AgeRng4"] = "50-59"
    #df["Symptoms1"] = #ICD10 R05 Cough
    #df["Symptoms2"] = #ICD10 R06.02 Shortness of Breath 
    #df["Symptoms3"] = #ICD10 R09.81 Congestion/Runny Nose 
    #df["Symptoms4"] = #ICD10 R43 Change in Taste/Smell 
    #df["Symptoms5"] = #ICD10 R07 Sore Throat 
    #df["Symptoms6"] = #ICD10 R11 Nausea/Vomiting 
    #df["Symptoms7"] = #ICD10 R19.7 Diarrhea 
    #df["Symptoms8"] = #ICD10 R50.9 Fever 
    #df["Symptoms9"] = #ICD10 R51 Headache 
    #df["Symptoms10"] = #ICD10 R52 Muscle Aches

# Ensure numeric targets
    for col in ["Target1", "Target2"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

# Compute Log10VL per row
    df["Log10VL"] = df.apply(lambda r: _safe_log10_mean(r.get("Target1"), r.get("Target2")), axis=1)

# Keep columns we’ll align to schema later (others will be added by enforce_schema)
    frames.append(df[[
        "StudyID", "PersonID", "Pathogen", "PtSpecies",
        "TimeDays", "SampleSource1", "SampleMethod",
        "Platform", "DOI", "Target1", "Target2", "Log10VL", "Units"
    ]])

    out = pd.concat(frames, ignore_index=True)

# Re-baseline TimeDays so that first detected positive per person = 0
# "Detected" = Target1 or Target2 present and > 0 (after coercion)
    def first_detected_day(g):
        mask = ((g["Target1"].fillna(-1) > 0) | (g["Target2"].fillna(-1) > 0)) & g["TimeDays"].notna()
        if mask.any():
            return g.loc[mask, "TimeDays"].min()
        return np.nan

    shifts = out.groupby("PersonID", dropna=False).apply(first_detected_day).rename("t0")
    out = out.merge(shifts, on="PersonID", how="left")
    out["TimeDays"] = pd.to_numeric(out["TimeDays"], errors="coerce") - pd.to_numeric(out["t0"], errors="coerce")
    out.drop(columns=["t0"], inplace=True)

    # Final schema alignment
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
    print(f"Loaded Savela et al. 2022 — {len(df_infection)} total rows.")
    return df_infection


if __name__ == "__main__":
    df = load_and_format()
    print(df.head(15))
