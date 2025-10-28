# WIP - Carolyn
# NEED TO DO: Pull data from https://github.com/VirologyCharite/SARS-CoV-2-VL-paper/tree/main/data

import pandas as pd
from schema import enforce_schema, coerce_types

def load_and_format():
    # Import the raw data:
    df = pd.read_csv("data/jones2021.csv")

    # Keep only the columns we need: 
    df = df[['patient', 'sample_type', 'log10_viral_load', 'days_since_symptom']]

    # redo patient ID to numerical instead of alphabetical


    # Map the contents of column sample_type to standard names: 
    df["SampleType"] = df["SampleType"].replace({
        "sputum": "tbd", # throat vs. saliva vs. lung?
        "swab": "tbd"
        })

    # Rename columns to match schema: 
    df = df.rename(columns={
        "patient": "PersonID",
        "days_since_symptom": "TimeDays" # correct use?
        # more?
        })

    # Add additional columns with known but missing information:
    df["StudyID"] = "jones2021"
    df["DOI"] = "10.1126/science.abi5273"
    
    # more to add here ...

    df = enforce_schema(df)
    df = coerce_types(df)
    return df