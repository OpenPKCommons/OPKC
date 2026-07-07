"""
Wagstaffe et al. 2024 (DOI: 10.1126/sciimmunol.adj9285)
========================================================
Paper overview:
---------------
This study examined how prior vaccination and infection shape
mucosal and systemic immune responses to SARS-CoV-2, including
effects on viral clearance and immune memory.

Data source:
------------
- https://www.science.org/doi/10.1126/sciimmunol.adj9285

Notes:
- Species: Human
- Units: Antibody titers, viral RNA Ct values
- Sampling: Nasal swabs, blood, mucosal samples
- Platform: RT-qPCR, ELISA, neutralization assays
- Targets: Spike and nucleocapsid
- No public raw viral load dataset released
"""
import pandas as pd
import os
from schema import enforce_schema, coerce_types

def load_and_format():
    # Import the raw data:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    df = pd.read_csv(os.path.join(base_dir, "data", "wagstaffe2024.csv"))

    # Keep only the columns we need (all in this case): 
    df = df[['PersonID', 'DaysPostInoculation', 'GEml', 'site']]
    # for each individual we have 1 to 19.5 DaysPostInoculation data points with corresponding GEml (NA if not available)
    # Virological assessments of infections were based on 12-­ hour mid-turbinate and throat flocked swabs

    # Map the contents of column site (to be SampleType) to standard names: 
    df["site"] = df["site"].replace({
        "nose": "nose", # interchangeable refer to this as mid-turbinate
        "throat": "throat" # need to confirm vs oropharyngeal -> see issue. Killingley et al also not any more specific
        })

    # Rename columns to match schema: 
    df = df.rename(columns={
        "PersonID": "IndivID",
        "DaysPostInoculation": "TimeDays",
        "GEml": "BiomarkerQuantity", # is log10VL
        "site": "SampleSource"
        })

    # Add additional columns with known but missing information:
    df["StudyID"] = "Wagstaffe2024"
    df["Pathogen"] = "SARS-CoV-2"
    df["IndivSpecies"] = "Human"
    df["DOI"] = "10.1126/sciimmunol.adj9285"
    df["Units"] = "GEml (log10VL)"
    df["AssayType"] = "RT-qPCR"
    df["SampleMethod"] = "flocked_swab_in_VTM"

    # For reference...
    # ACTIVATION TIME
        # throat: 1.78 days
        # nose: 2.61 days
    # VIRAL LOAD GROWTH RATE
        # throat: 5.41 days^-1
        # nose: 4.86 days^-1
    # PEAK TIME (ESTIMATED)
        # throat: 3.4 days
        # nose: 5.1 days
    # PEAK VIRAL LOAD
        # throat: 6.96 log_10
        # nose: 8.69 log_10
    # VIRAL LOAD DECAY RATE
        # throat: 0.69 days^-1
        # nose: 1.29 days^-1

    df["Biomarker"] = "pathogen load"
    df = enforce_schema(df)
    df = coerce_types(df)
    
    return df