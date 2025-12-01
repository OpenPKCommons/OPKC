# Alahakoon 2025
# Data source: https://github.com/PunyaAlahakoon/west_nile_virus_abm/tree/main

# Data formatted from alahakoon2025_rawfiles
# Column names of combined Alahakoon 2025 data for reference

# WIP!

import pandas as pd
from schema import enforce_schema, coerce_types

def load_and_format():
    # Import the raw data:
    df = pd.read_csv("data/puhach2022.csv")

    # Keep only the columns we need: 
    df = df[['sample number', 'DPOS', 'Variant', 'FFU/ml', 'Age']] # collection_date, disease_week, species, sex_condition, ctval, num_count (number of individuals?)

    # Rename columns to match schema: 
    df = df.rename(columns={
        "sample number": "PersonID",
        "DPOS": "TimeDays",
        "FFU/ml": "PathogenLoad", # log10 genome copies per ml for RNA viral loads
        "Variant": "Subtype",
        "Age": "AgeRng1"
        })

    # Add additional columns with known but missing information:
    df["StudyID"] = "puhach2022"
    df["Pathogen"] = "SARS2"
    df["IndSpecies"] = "Human"
    df["Units"] = "GEml (log10VL)"
    df["DOI"] = "10.1038/s41591-022-01816-0"
    df["PlatformType"] = "RT-qPCR"
    df["PlatformTech"] = "Roche cobas 6800/"
    df["Targets"] = "E-gene, S-gene"

    df = enforce_schema(df)
    df = coerce_types(df)
    return df