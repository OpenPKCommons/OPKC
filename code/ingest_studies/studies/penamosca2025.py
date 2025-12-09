"""
Peña-Mosca et al. 2025 (DOI: 10.1038/s41467-025-61553-z)
========================================================
Paper overview:
---------------
This study investigated the impact of highly pathogenic avian influenza (HPAI)
H5N1 virus infection in an Ohio dairy herd during a March-April 2024 outbreak.
The study documented clinical disease in 20.0% (777/3876) adult cows, with 
seroprevalence of 89.4% (570/637), indicating widespread subclinical infection.
Significant milk production losses (~900 kg per cow) and economic impacts were
recorded.

Data source:
------------
- https://github.com/fepenamosca/hpai_impact_dairies/tree/fd5f303f4aae47ef3a6259e7e7b94284f8c3af67/data
- https://www.nature.com/articles/s41467-025-61553-z
- Extended Data Table 1: individual animal data including viral loads

Notes:
- Data is in extended_data_table_1.xlsx, renamed to 'penamosca2025.xlsx'
- Study focused on H5N1 clade 2.3.4.4b in dairy cattle
- Viral loads measured in milk samples using RT-qPCR
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
def penamosca2025():
    """Load and format HPAI H5N1 viremia data from Peña-Mosca et al. 2025."""

    xlsx_path = os.path.join(base_dir, "data", "penamosca2025.xlsx")
    df = pd.read_excel(xlsx_path) 

    if "sample" in df.columns:
        sample = df["sample"].astype(str).str.lower()

        df["SampleSource"] = sample.map({
          "milk": "milk",
          "nasal_swab": "nares",
           "whole_blood": "blood",
           "feces": "feces",
           "urine": "urine",
           "serum": "serum",
      })

        df["SampleMethod"] = sample.map({
           "milk": "milk sample",
           "nasal_swab": "nasal swab",
           "whole_blood": "blood draw",
           "feces": "fecal collection",
           "urine": "urine collection",
           "serum": "blood draw (serum)",
      })

    # Rename columns to match schema
    rename_map = {
        "id": "IndivID",
        "ct_pcr": "PathogenLoad",
    }

    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    # Convert PathogenLoad (Ct values) to numeric, with negative results or missing Ct values becoming NA
    df["PathogenLoad"] = pd.to_numeric(df["PathogenLoad"], errors="coerce")
    df.loc[df["PathogenLoad"] <= 0, "PathogenLoad"] = pd.NA 

    # Calculate TimeDays from sample_date and date_gripa_cow (disease onset date)
    df["sample_date"] = pd.to_datetime(df["sample_date"], errors="coerce")
    df["date_gripa_cow"] = pd.to_datetime(df["date_gripa_cow"], errors="coerce")
    df["TimeDays"] = (df["sample_date"] - df["date_gripa_cow"]).dt.days

    # Construct SampleID 
    df["SampleID"] = df["IndivID"].astype(str) + "_" + df["TimeDays"].astype(str)

    df["StudyID"] = "penamosca2025"
    df["Pathogen"] = "Flu"
    df["IndSpecies"] = "Dairy cattle"
    df["DOI"] = "10.1038/s41467-025-61553-z"
    df["PlatformType"] = "RT-qPCR"
    df["Subtype"] = "H5N1"
    
    # Units (Ct values, 'cycle threshold')
    df["Units"] = "Ct"

    # Enforce schema and coerce types
    df = enforce_schema(df)
    df = coerce_types(df)

    return df


# %%
def load_and_format():
    df = penamosca2025()
    return df


# %%
