"""
Wongnak et al. 2024 (DOI: 10.1016/S1473-3099(24)00183-X)
========================================================
Paper overview:
---------------
This study evaluated SARS-CoV-2 viral kinetics in hospitalized
patients infected with contemporary variants, linking viral
burden to disease severity and clinical outcomes.

Data source:
------------
- https://www.thelancet.com/journals/laninf/article/PIIS1473-3099(24)00183-X

Notes:
- Species: Human
- Units: Viral RNA copies per mL
- Sampling: Serial respiratory specimens
- Platform: RT-qPCR
- Targets: SARS-CoV-2 nucleocapsid gene
- Clinical cohort with outcome stratification
"""
import pandas as pd
from schema import enforce_schema, coerce_types

def load_and_format():
    # Import the raw data:
    df = pd.read_csv("data/wongnak2024.csv")

    # Keep only the columns we need: 
    df = df[['ID', 'Time', 'Trt', 'Swab_ID', 'Age', 'BARCODE', 'Variant', 'log10_viral_load']]

    # Rename columns to match the standard schema:
    df = df.rename(columns={
        "ID": "IndivID",
        "Time": "TimeDays",
        "Trt": "Treatment1",
        "Swab_ID": "SampleSource", #they specify which tonsil, but oropharyngeal would suffice
        "Age": "AgeRng1",
        "BARCODE": "SampleID", 
        "Variant": "Subtype",
        "log10_viral_load": "PathogenLoad"
        })

    # Since age is given as a single value, set the upper bound of the age range to be the same
    df['AgeRng2'] = df['AgeRng1']

    # Add additional columns with known but missing information:
    df["StudyID"] = "wongnak2024"
    df["Pathogen"] = "SARS2"
    df["IndSpecies"] = "Human"
    df["DOI"] = "10.1016/S1473-3099(24)00183-X"
    df["Units"] = "GEml (log10VL)"
    df["SampleMethod"] = "flocked_OP_swab_in_VTM" #Swabs = Thermo Fisher MicroTest and COPAN FLOQSwabs, VTm = Thermo Fisher M4RT viral transport medium (3 mL)
    df["PlatformType"] = "RT-qPCR"
    df["PlatformTech"] = "TaqCheckFastPCR"
    df["Targets"] = "N, S"

    df = enforce_schema(df)
    df = coerce_types(df)

    return df