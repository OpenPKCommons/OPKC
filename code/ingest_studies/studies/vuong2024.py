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
import numpy as np
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
        "vir": "BiomarkerQuantity",
        "Serotype": "PathogenSubtype"
    }

    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    # Source viremia is in linear-scale copies/mL. Log10-transform for
    # consistency with wongnak/waickman etc. so downstream plots and fits share
    # a common y-axis scale.
    #
    # BLOD is detected on the *linear-scale* source: source <= 0 is a sentinel
    # for "not detected". log10 is undefined for these, so BiomarkerQuantity
    # stays NaN for BLOD rows but BelowLOD is flagged. LOD_min in log10 units
    # isn't well-defined (log10(0) is -inf), so left as NA.
    src = pd.to_numeric(df["BiomarkerQuantity"], errors="coerce")
    df["BelowLOD"] = src.le(0).where(src.notna(), pd.NA)
    df["BiomarkerQuantity"] = np.log10(src.where(src > 0))

    # Construct SampleID 
    df["SampleID"] = df["IndivID"].astype(str) + "_" + df["TimeDays"].astype(str)

    df["StudyID"] = "Vuong2024"
    df["Pathogen"] = "Dengue"
    df["IndivSpecies"] = "Human"
    df["SampleSource"] = "serum"
    df["SampleMethod"] = "blood draw (serum)"
    df["DOI"] = "10.7554/eLife.92606"
    df["AssayType"] = "RT-qPCR"
    df["AgeRng1"] = df["Age"]
    df["AgeRng2"] = df["Age"]

    df["Units"] = "log10(copies/mL)"

    # Enforce schema and coerce types
    df["Biomarker"] = "pathogen load"
    df = enforce_schema(df)
    df = coerce_types(df)

    return df


# %%
def load_and_format():
    df = vuong2024()
    return df

# %%