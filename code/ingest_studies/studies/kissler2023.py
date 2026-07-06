"""
Kissler et al. 2023 (DOI: 10.1038/s41467-023-41941-z)
========================================================
Paper overview:
---------------
This study compared viral load dynamics between SARS-CoV-2
variants, including Omicron sublineages, to assess infectious
period and transmission potential using longitudinal testing.

Data source:
------------
- https://www.nature.com/articles/s41467-023-41941-z

Notes:
- Species: Human
- Units: Ct values converted to viral RNA copies/mL
- Sampling: Longitudinal self-collected nasal swabs
- Platform: RT-qPCR
- Targets: N1/N2 SARS-CoV-2 genes
- No public standalone dataset
"""
import pandas as pd
import os
from schema import enforce_schema, coerce_types

def load_and_format():
    # Import the raw data:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    df = pd.read_csv(os.path.join(base_dir, "data", "kissler2023.csv"))

    # Keep only the columns we need: 
    df = df[['PersonID', 'InfectionEvent', 'TestDateIndex', 'CtT1', 'AgeGrp', 'LineageBroad']]

    # Format the age group column into separate age ranges: 
    df[["AgeRng1", "AgeRng2"]] = df["AgeGrp"].str.extract(r"[\[\(](\d+),\s*(\d+)[\)\]]")

    # Convert to numeric
    df["AgeRng1"] = pd.to_numeric(df["AgeRng1"], errors="coerce")
    df["AgeRng2"] = pd.to_numeric(df["AgeRng2"], errors="coerce")

    # Rename columns to match schema: 
    df = df.rename(columns={
        "PersonID": "IndivID",
        "InfectionEvent": "InfectionID",
        "TestDateIndex": "TimeDays",
        "CtT1": "BiomarkerQuantity",
        "LineageBroad": "PathogenSubtype"
        })

    # Add additional columns with known but missing information:
    df["StudyID"] = "kissler2023"
    df["Pathogen"] = "SARS-CoV-2"
    df["IndivSpecies"] = "Human"
    df["DOI"] = "10.1038/s41467-023-41941-z"
    df["Units"] = "Ct"
    df["AssayType"] = "RT-qPCR"
    df["ReadoutPlatform"] = "cobas_target1"
    df["GEml_conversion_intercept"] = 11.34089
    df["GEml_conversion_slope"] = -0.2770306
    df["SampleSource"] = "nasal+oropharyngeal"
    df["SampleMethod"] = "swab in VTM"
    df["AssayTargets"] = "E484K, N501Y, delHV-69/70"
    

    df["Biomarker"] = "pathogen load"
    df = enforce_schema(df)
    df = coerce_types(df)
    return df