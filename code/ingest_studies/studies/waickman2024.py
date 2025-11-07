"""
Waickman et al. 2024 (DOI: 10.1038/s41564-024-01668-z)
====================================================================
Study summary:
---------------
This controlled human infection model (CHIM) study evaluated immune
and virologic responses to Dengue virus serotype-1 (DENV-1) strain
CH53489 challenge in vaccinated and unvaccinated participants.
The goal was to identify correlates of protection by comparing
post-challenge viral kinetics, NS5-specific ELISPOT responses,
and other immunological endpoints.

Dataset included here corresponds to Fig. 6a–d: correlation between
peak viremia (PFU mL⁻¹, log₁₀) and NS5 ELISPOT counts (SFC per 10⁶ PBMC).

Temporal variable:
-------------------
• Time variable is not explicitly included — each row represents a
  single participant-level summary point (peak viremia vs. day 90 ELISPOT).

Data source:
------------
Raw dataset: Supplementary Data 6 (Excel file: “41564_2024_1668_MOESM6_ESM.xlsx”;
locally renamed to `waickman2024.xlsx`), available from 
https://www.nature.com/articles/s41564-024-01668-z under "Source Data."
Listed as “Statistical source data for Figs. 1–6 and Extended Figs. 1–2 and 5.”

Key variables:
--------------
• Viremia — peak viral load (log₁₀ PFU mL⁻¹)
• NS5 ELISPOT — NS5-specific IFN-γ spot-forming cells (SFC per 10⁶ PBMC)

Notes:
------
• Participants 301–309 correspond to nine individuals included in the challenge cohort.
• Data derived from Fig. 6a–d (Waickman et al. 2024, Nat Microbiol).
• Each row = one participant; no longitudinal component.
"""

import os, sys
import pandas as pd

# Make parent folder importable to import schema.py
THIS_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.abspath(os.path.join(THIS_DIR, ".."))
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from schema import enforce_schema, coerce_types


def load_and_format(base_dir=None):
    """Load correlation dataset between viremia and NS5 ELISPOT (Fig. 6a–d)."""
    if base_dir is None:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    xlsx_path = os.path.join(base_dir, "data", "waickman2024.xlsx")
    df_raw = pd.read_excel(xlsx_path)

    # Drop empty rows and reshape wide-to-long
    df_raw = df_raw.dropna(how="all")
   # Reshape from wide to long format
    df_raw.columns = df_raw.columns.map(str)
    df = df_raw.melt(id_vars="Day", var_name="PersonID", value_name="Log10VL")
    df = df.dropna(subset=["Log10VL"])
    df["PersonID"] = df["PersonID"].astype(int)
    df["TimeDays"] = df["Day"]
    df = df.drop(columns=["Day"])

    # Replace 1.0 baseline (non-detectable) values with NaN
    df.loc[df["Log10VL"] <= 1.0, "Log10VL"] = pd.NA

    # Core metadata
    df["StudyID"] = "waickman2024"
    df["Pathogen"] = "Dengue"
    df["PtSpecies"] = "human"
    df["InfectionID"] = pd.NA
    df["SampleID"] = pd.NA
    # Symptomatic status reported at cohort level (fever, headache, rash, fatigue), data not available per participant
    # df["Symptoms1"] = "R21" #ICD10 R21 Rash
    # df["Symptoms2"] = "R53" #ICD10 R53 Fatigue
    # df["Symptoms3"] = "R51" #ICD10 R51 Headache
    # df["Symptoms4"] = "R50.9" #ICD10 R50.9 Fever
    df["Comorbidity1"] = pd.NA
    df["Comorbidity2"] = pd.NA
    df["Comorbidity3"] = pd.NA
    df["Comorbidity4"] = pd.NA
    df["Treatment1"] = "Acetaminophen"
    df["Treatment2"] = "Oral fluids"
    df["Treatment3"] = pd.NA
    df["Treatment4"] = pd.NA
    df["SampleSource"] = "serum"
    df["SampleMethod"] = "blood draw (serum)"
    df["AgeRng1"] = 18
    df["AgeRng2"] = 45
    df["Subtype"] = "DENV-3 CH53489"
    df["PlatformName"] = "RT-qPCR"
    df["DOI"] = "10.1038/s41564-024-01668-z"
    df["Units"] = "GE/ml"
    df["GEml_conversion_intercept"] = pd.NA
    df["GEml_conversion_slope"] = pd.NA
    df["Targets"] = "DENV-3 genome (RNA)"
    df["PlatformTech"] = "In-house qRT-PCR, Vero plaque assay"

    # Hospitalization status (from Supplemental Table 4)
    hospitalized_map = {
        301: "N", 302: "Y", 303: "Y", 304: "Y", 305: "Y",
        306: "N", 307: "N", 308: "Y", 309: "Y"
    }
    df["Hospitalized"] = df["PersonID"].map(hospitalized_map)

    # Optional: Peak viral load (GE/mL) from Supplemental Table 4
    peak_vl = {
        301: 1.37e5, 302: 7.02e8, 303: 6.89e7, 304: 3.65e7,
        305: 3.51e8, 306: 2.94e5, 307: 3.13e4, 308: 7.41e5, 309: 4.57e7
    }
    df["PeakVL_GEml"] = df["PersonID"].map(peak_vl)

# Note: RNAseq transcriptomic profiling was performed in a parallel analysis
# (host gene expression study, Supplementary Table 4) but is not included here,
# as this ingestion represents qRT-PCR-derived viral load measurements only.

    # Apply schema checks
    df = enforce_schema(df)
    df = coerce_types(df)

    return df

if __name__ == "__main__":
    df = load_and_format()
    print(df.head(10))