"""
Vuong et al. 2024 (DOI: 10.7554/eLife.92606)
========================================================
Paper overview:
---------------
This study analysed viremia kinetics and clinical outcomes in
2340 dengue patients from three cohort studies in Vietnam.
Longitudinal plasma viremia was quantified using RT-PCR,
with illness day measured relative to symptom onset.

Data source:
------------
- https://github.com/Nguyenlamvuong/Dengue_Viremia_Kinetics_eLife_2024/tree/main
- https://elifesciences.org/articles/92606 

Notes:
- Data is in Longitudinal viremia and platelet 22May2024.csv which feeds all
  viremia trajectory plots in the paper (Fig 1A-C, 2A, and supplementary)
  renamed to 'vuong2024.csv' for clarity.
- PlatformTech unspecified, paper reports the following:
    Studies A and B: Internally controlled, serotype-specific, real-time, two-step assay
    Study C: One-step procedure using a validated assay

"""


# %%
import pandas as pd
import sys
from pathlib import Path
import os

# Make parent folder importable to import schema.py
THIS_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.abspath(os.path.join(THIS_DIR, ".."))  # ../ingest_studies
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from schema import enforce_schema, coerce_types

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))


# %%
def vuong2024():
    """Load and format longitudinal plasma viremia data from Vuong et al. 2024."""

    csv_path = os.path.join(base_dir, "data", "vuong2024.csv")
    df = pd.read_csv(csv_path)

    # Rename columns to match schema
    rename_map = {
        "Code": "IndivID",
        "DOI": "TimeDays",
        "vir": "PathogenLoad",
        "Serotype": "Subtype"
    }

    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    # Below detection limit is NA
    df["PathogenLoad"] = pd.to_numeric(df["PathogenLoad"], errors="coerce")
    df.loc[df["PathogenLoad"] <= 0, "PathogenLoad"] = pd.NA

    # Construct SampleID 
    df["SampleID"] = df["IndivID"].astype(str) + "_" + df["TimeDays"].astype(str)

    df["StudyID"] = "vuong2024"
    df["Pathogen"] = "Dengue"
    df["IndSpecies"] = "human"
    df["SampleSource"] = "serum"
    df["SampleMethod"] = "blood draw (serum)"
    df["DOI"] = "10.7554/eLife.92606"
    df["PlatformType"] = "RT-qPCR"
    df["AgeRng1"] = df["Age"]
    df["AgeRng2"] = df["Age"]

    # Units (raw RNA copies per ml)
    df["Units"] = "copies/ml"

    # Enforce schema and coerce types
    df = enforce_schema(df)
    df = coerce_types(df)

    return df


# %%
def load_and_format():
    df = vuong2024()
    return df

# %%