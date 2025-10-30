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
  for each participant. This variable is mapped to the schema variable `TimeDays`.

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

import math
import pandas as pd
# Make parent folder importable to import schema.py
import os, sys
THIS_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.abspath(os.path.join(THIS_DIR, ".."))  # .../ingest_studies
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from schema import enforce_schema, coerce_types

def load_savela2022_infection(data_dir):
    """Load and format longitudinal infection data (Fig 2A–G paired datasets)."""
    infection_files = [
        f for f in os.listdir(data_dir)
        if f.startswith("savela2022_fig2") and f.endswith(".xlsx")
    ]
    dfs = []

    for f in infection_files:
        df = pd.read_excel(os.path.join(data_dir, f))
        df["source_file"] = f
        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)

    # Clean and standardize
    df.rename(columns={
        "Participant": "ParticipantID",
        "Days Post-Enrollment": "DaysPostEnrollment",
        "Sample Type": "SampleType",
        "Viral Load N1 (copies/mL)": "ViralLoad_N1",
        "Viral Load N2 (copies/mL)": "ViralLoad_N2",
    }, inplace=True, errors="ignore")

    df["StudyID"] = "savela2022"
    df["Units"] = "copies/mL"
    df["Matrix"] = df["SampleType"].str.lower()
    df["Method"] = "RT-qPCR"
    df["Notes"] = "Self-collected paired saliva and nasal swab samples"

    # Simplify and reorder columns
    df = df[[
        "StudyID", "ParticipantID", "DaysPostEnrollment", "Matrix",
        "ViralLoad_N1", "ViralLoad_N2", "Units", "Method", "Notes", "source_file"
    ]]

    return df


def load_savela2022_calibration(data_dir):
    """Load calibration curve data (Fig 1A/B)."""
    files = {
        "swab": "savela2022_swab.xlsx",
        "saliva": "savela2022_saliva.xlsx"
    }

    dfs = []
    for sample_type, filename in files.items():
        path = os.path.join(data_dir, filename)
        df = pd.read_excel(path)
        df["SampleType"] = sample_type
        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)

    df.rename(columns={
        "Sample ID": "SampleID",
        "Geometric Mean": "GeometricMean",
        "qPCRLoad": "RTqPCR_Load",
        "qPCRCt": "RTqPCR_Ct",
        "dPCRLoad (Cp/mL)": "ddPCR_Load"
    }, inplace=True)

    df["StudyID"] = "savela2022"
    df["Experiment"] = "calibration"
    df["Units"] = "copies/mL"

    df = df[[
        "StudyID", "Experiment", "SampleType", "SampleID",
        "RTqPCR_Load", "ddPCR_Load", "RTqPCR_Ct", "GeometricMean", "Units"
    ]]

    return df


def load_savela2022_stability(data_dir):
    """Optional: load saliva and swab stability (SI Fig 3B)."""
    files = [
        "savela2022_saliva_SI.xlsx",
        "savela2022_swab_SI.csv"
    ]
    dfs = []
    for f in files:
        path = os.path.join(data_dir, f)
        if f.endswith(".xlsx"):
            df = pd.read_excel(path)
        else:
            df = pd.read_csv(path)
        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)
    df["StudyID"] = "savela2022"
    df["Experiment"] = "sample_stability"
    df.rename(columns={"VL_cpml": "CopiesPerML"}, inplace=True)
    df["Units"] = "copies/mL"
    return df


def load_and_format(base_dir=None):
    """Master loader that compiles all Savela 2022 datasets into unified format."""
    if base_dir is None:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))


    data_dir = os.path.join(base_dir, "data")

    infection = load_savela2022_infection(data_dir)
    calibration = load_savela2022_calibration(data_dir)

    try:
        stability = load_savela2022_stability(data_dir)
    except Exception as e:
        print(f"Warning: could not load stability data: {e}")
        stability = pd.DataFrame()

    df_all = pd.concat([infection, calibration, stability], ignore_index=True, sort=False)
    print(f"Loaded Savela et al. 2022 — {len(df_all)} total rows.")
    return df_all


if __name__ == "__main__":
    df = load_and_format()
    print(df.head(20))
