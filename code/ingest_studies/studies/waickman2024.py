"""
Waickman et al. 2024 (DOI: 10.1038/s41564-024-01668-z)
====================================================================
Study summary:
---------------
This dengue human infection model (DHIM) study examined the viral,
infectious, and NS1 antigenemia kinetics following subcutaneous
challenge of adults with Dengue virus serotype-3 (DENV-3) strain CH53489.

Dataset corresponds to Fig. 1 (viral kinetics):
• Figure 1B: DENV-3 RNAemia (RT-qPCR)
• Figure 1C: Infectious viraemia (Vero plaque assay)
• Figure 1D: NS1 antigenemia (ELISA)

Excluded: Figure 1E–F (onset/peak summaries; not longitudinal).

Temporal variable:
-------------------
• TimeDays = days post-inoculation.

Data source:
------------
Raw dataset: “waickman2024.xlsx”
("Source Data" from Waickman et al. 2024, Nat Microbiol).

• Symptoms and treatments not time-resolved; excluded per schema.
• Values of 1 represent “below limit of detection” and are set to NA.
"""

import os, sys
import pandas as pd

# Make parent folder importable for schema
THIS_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.abspath(os.path.join(THIS_DIR, ".."))
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from schema import enforce_schema, coerce_types


def _load_sheet(base_dir, sheet_name, platform_type, units, platform_tech, targets):
    xlsx_path = os.path.join(base_dir, "data", "waickman2024.xlsx")
    df_raw = pd.read_excel(xlsx_path, sheet_name=sheet_name)
    df_raw = df_raw.dropna(how="all")
    df_raw.columns = df_raw.columns.map(str)
    df_raw = df_raw.loc[:, ~df_raw.columns.str.contains("^Unnamed")]
    id_cols = [c for c in df_raw.columns if c.isdigit()]

    df = df_raw.melt(id_vars="Day", value_vars=id_cols, var_name="IndivID", value_name="PathogenLoad")
    df["TimeDays"] = df["Day"]
    df = df.drop(columns=["Day"])

    # Replace BLOD / non-detectable values ≤1 with NaN
    df["PathogenLoad"] = pd.to_numeric(df["PathogenLoad"], errors="coerce")
    df.loc[df["PathogenLoad"] <= 1.0, "PathogenLoad"] = pd.NA # or zero?

    # Core metadata
    df["StudyID"] = "waickman2024"
    df["Pathogen"] = "Dengue"
    df["IndSpecies"] = "human"
    # df["Symptoms1"] = "R51"     # Headache
    # df["Symptoms2"] = "R21"     # Rash
    # df["Symptoms3"] = "R50.9"   # Fever
    # df["Symptoms4"] = "R53.83"   # Fatigue
    df["SampleSource"] = "serum"
    df["SampleMethod"] = "blood draw (serum)"
    df["AgeRng1"] = 18
    df["AgeRng2"] = 45
    df["Subtype"] = "DENV-3 CH53489"
    df["PlatformType"] = platform_type
    df["DOI"] = "10.1038/s41564-024-01668-z"
    df["Units"] = units
    df["Targets"] = targets
    df["PlatformTech"] = platform_tech

    df = enforce_schema(df)
    df = coerce_types(df)
    return df


def load_and_format(base_dir=None):
    """
    Load viral kinetics dataset for Waickman 2024 (Fig 1B–D).
    """
    if base_dir is None:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))

    sheets = [
        ("Figure 1B", "RT-qPCR", "GE/ml (log10)", "fluorogenic dengue type-specific RT-qPCR",
         "DENV-3 genome (RNA)"),
        ("Figure 1C", "plaque-forming assay", "PFU/ml", "Vero cell plaque assay",
         "Infectious DENV-3 particles"),
        ("Figure 1D", "ELISA", "OD (ELISA units)", "NS1 capture ELISA",
         "DENV-3 NS1 protein"),
    ]

    dfs = []
    for sheet, platform_type, units, platform_tech, targets in sheets:
        dfs.append(_load_sheet(base_dir, sheet, platform_type, units, platform_tech, targets))

    df_all = pd.concat(dfs, ignore_index=True)
    return df_all

"""
if __name__ == "__main__":
    df = load_and_format()
    print(df.head(10))
"""
