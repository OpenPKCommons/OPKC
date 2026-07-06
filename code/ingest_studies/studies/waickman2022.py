"""
Waickman et al. 2022 (DOI: 10.1126/scitranslmed.abo5019)
====================================================================
Study summary:
---------------
This dengue human infection model (DHIM) study evaluated the safety and
virologic/immunologic kinetics following challenge of flavivirus-naive
adults with Dengue virus serotype-1 (DENV-1) strain 45AZ5.
Nine volunteers received a single subcutaneous inoculation.

Dataset corresponds to Fig. 1 (viremia and RNAemia kinetics following
DENV-1 challenge). 
• Figure 1a: DENV-1 RNAemia (RT-qPCR)
• Figure 1b: DENV-1 Viremia (Vero plaque assay)
• Figure 1c: NS1 antigenemia (ELISA)

Excluded: Figures 2-6. Immunological and inflammatory response datasets
(IgM/IgG/IgA) ELISA, ELISPOT, cytokine panels, correlation analyses)
These represent host immune or inflammatory responses, not pathogen load.

Temporal variable:
-------------------
• TimeDays = days post-inoculation.

Data source:
------------
Raw dataset: Supplementary Data S1 (Excel file “waickman2022_s1.xlsx”),
available with Waickman et al. 2022 Sci Transl Med.

• Symptoms (headache, rash, fever, eye pain, weakness/fatigue, myalgia) reported
  but not time-resolved; commented out below.
• Treatments: acetaminophen, oral fluids, antinausea medication reported but not
  time-resolved and not given to all participants; commented out below.
• "BelowLOD" = below limit of detection
"""

import os, sys
import pandas as pd

# Make parent folder importable to import schema.py
THIS_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.abspath(os.path.join(THIS_DIR, ".."))
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from schema import enforce_schema, coerce_types


def _load_sheet(base_dir, sheet_name, platform_type, units, readout_platform, targets):
    xlsx_path = os.path.join(base_dir, "data", "waickman2022_s1.xlsx")
    df_raw = pd.read_excel(xlsx_path, sheet_name=sheet_name)
    df_raw = df_raw.dropna(how="all")
    df_raw.columns = df_raw.columns.map(str)

    df = df_raw.melt(id_vars="Study day", var_name="IndivID", value_name="BiomarkerQuantity")
    df["TimeDays"] = df["Study day"]
    df = df.drop(columns=["Study day"])

    # Flag values below the assay's LOD instead of destroying them. Preserve the
    # raw reported number.
    lod_min = 1.0  # log10VL floor: values at or below this are below the LOD
    df["BiomarkerQuantity"] = pd.to_numeric(df["BiomarkerQuantity"], errors="coerce")
    df["LOD_min"] = lod_min
    df["BelowLOD"] = df["BiomarkerQuantity"].le(lod_min).where(df["BiomarkerQuantity"].notna(), pd.NA)

    # Core metadata
    df["StudyID"] = "waickman2022"
    df["Pathogen"] = "Dengue"
    df["IndivSpecies"] = "human"
    # df["Symptoms1"] = "R51"     # Headache
    # df["Symptoms2"] = "R21"     # Rash
    # df["Symptoms3"] = "R50.9"   # Fever
    # df["Symptoms4"] = "H57.1"   # Eye pain
    # df["Treatment1"] = "Acetaminophen"
    # df["Treatment2"] = "Oral fluids"
    # df["Treatment3"] = "Antinausea medication"
    df["SampleSource"] = "serum"
    df["SampleMethod"] = "blood draw (serum)"
    df["AgeRng1"] = 20
    df["AgeRng2"] = 45
    df["PathogenSubtype"] = "DENV-1 45AZ5"
    df["AssayType"] = platform_type
    df["DOI"] = "10.1126/scitranslmed.abo5019"
    df["Units"] = units
    df["ReadoutPlatform"] = readout_platform
    df["AssayTargets"] = targets
    
    df["Biomarker"] = "pathogen load"
    df = enforce_schema(df)
    df = coerce_types(df)
    return df


def load_and_format(base_dir=None, include_onset=False):
    """
    Load viral-kinetics data from Waickman 2022 (Fig 1A–C).
    """
    if base_dir is None:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))

    sheets = [
        ("Figure 1a PCR", "RT-qPCR", "GE/ml (log10)", "fluorogenic dengue type-specific RT-qPCR",
         "DENV-1 genome (RNA)"),
        ("Figure 1b Plaque", "plaque-forming assay","PFU/ml", "Vero cell plaque assay",
         "Infectious DENV-1 particles"),
        ("Figure 1c", "ELISA", "OD (ELISA units)", "NS1 capture ELISA",
         "DENV-1 NS1 protein"),
    ]

    dfs = []
    for sheet, platform_type, units, platform_tech, targets in sheets:
        dfs.append(_load_sheet(base_dir, sheet, platform_type, units, platform_tech, targets))

    df_all = pd.concat(dfs, ignore_index=True)
    return df_all

"""
if __name__ == "__main__":
    df = load_and_format(include_onset=False)
    print(df.head(10))
"""