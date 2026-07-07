"""
Jones et al. 2021 (DOI: 10.1126/science.abi5273)
========================================================
Paper overview:
---------------
This study demonstrated that upper respiratory viral load of
SARS-CoV-2 is similar across age groups, including children and
adults, suggesting comparable transmission potential.

Data source:
------------
- https://www.science.org/doi/10.1126/science.abi5273

Notes:
- Species: Human
- Units: Viral RNA copies per mL
- Sampling: Diagnostic respiratory swabs
- Platform: RT-qPCR
- Target: SARS-CoV-2 ORF1ab
- Cross-sectional clinical testing dataset
"""
# Jones 2021
# Data source: https://github.com/VirologyCharite/SARS-CoV-2-VL-paper/tree/main

# Column names of Jones 2021 data for reference
# personHash , gender , PAMS1 , hospitalized , onset , B117 , date , viralLoad , age , testName , testCentre , testCentreCategory

import pandas as pd
import os
from schema import enforce_schema, coerce_types

def load_and_format():
    # Import the raw data:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    df = pd.read_csv(os.path.join(base_dir, "data", "jones2021.csv"))

    # Keep only the columns we need: 
    df = df[['personHash', 'onset', 'B117', 'date', 'viralLoad', 'age']] # redo patient ID to numerical instead of alphabetical - needed?

    # Compute TimeDays as days from a per-person reference date:
    #   (a) the person's earliest recorded symptom onset if any, otherwise
    #   (b) the person's earliest sample date (i.e., day 0 = first positive sample).
    # Onset is null for ~96% of rows in this dataset (mostly asymptomatic diagnostic
    # testing), so most rows fall back to (b).
    df["onset"] = pd.to_datetime(df["onset"])
    df["date"]  = pd.to_datetime(df["date"])
    first_onset = df.groupby("personHash")["onset"].transform("min")
    first_date  = df.groupby("personHash")["date"].transform("min")
    reference   = first_onset.fillna(first_date)
    df["computedTimeDays"] = (df["date"] - reference).dt.days

    df = df[['personHash', 'computedTimeDays', 'viralLoad', 'age', 'B117']]

    # Rename columns to match schema: 
    df = df.rename(columns={
        "personHash": "IndivID",
        "computedTimeDays": "TimeDays",
        "viralLoad": "BiomarkerQuantity", 
        "age": "AgeRng1"
        })
    
    # For B117-flagged rows, tag as Alpha lineage with the corresponding assay targets.
    df["PathogenSubtype"] = ""
    df.loc[df["B117"] == True, "PathogenSubtype"] = "B.1.1.7"

    df["AssayTargets"] = ""
    df.loc[df["PathogenSubtype"] == "B.1.1.7", "AssayTargets"] = "N501Y, del69/70 spike protein AA"

    # Add additional columns with known but missing information:
    df["StudyID"] = "Jones2021"
    df["Pathogen"] = "SARS-CoV-2"
    df["IndivSpecies"] = "Human"
    df["Units"] = "GEml (log10VL)" # intercepts available in supplemental material
    df["DOI"] = "10.1126/science.abi5273"
    df["AssayType"] = "RT-qPCR"
    # note that in data/jones2021_rawfiles, empirical culture data is recorded, confusingly labeled as "probabiliity"
    ## these were used to calculate the culture probability in the source paper, they are not simulated data
    ## not currently ingested here but could be added in future versions
    df["ReadoutPlatform"] = "Roche Light Cycler 480, or Roche cobas 6800/8800"
    # ~97% of samples are upper respiratory swabs (per paper Methods); the remaining
    # ~3% are lower respiratory tract samples from intubated patients. The raw data
    # doesn't distinguish per-row, so we use a single coarse URT label.
    df["SampleSource"] = "upper respiratory"
    df["SampleMethod"] = "swab"


    df["Biomarker"] = "pathogen load"
    df = enforce_schema(df)
    df = coerce_types(df)
    return df