# Jones 2021
# Data source: https://github.com/VirologyCharite/SARS-CoV-2-VL-paper/tree/main

# Column names of Jones 2021 data for reference
# personHash , gender , PAMS1 , hospitalized , onset , B117 , date , viralLoad , age , testName , testCentre , testCentreCategory

import pandas as pd
from schema import enforce_schema, coerce_types

def load_and_format():
    # Import the raw data:
    df = pd.read_csv("data/jones2021.csv")

    # Keep only the columns we need: 
    df = df[['personHash', 'onset', 'date', 'viralLoad', 'age']] # redo patient ID to numerical instead of alphabetical - needed?

    # Compute the days of the infection based on 'onset' and 'date'
    # convert datetime format
    df["onset"] = pd.to_datetime(df["onset"])
    df["date"] = pd.to_datetime(df["date"])
    # identify persons to loop over
    uniquePersons = df['personHash'].unique()
    # loop through each individual
    for val in uniquePersons:
        df_subset = df.loc[df['personHash'] == val]
        # determine date of symptom onset which is either the first element in onset...
        givenOnset = df_subset['onset'].iloc[0]
        # or the first element in date
        if pd.isnull(givenOnset):
            givenOnset = df_subset['date'].iloc[0]
        # Compute the difference for all elements in the subset
        # This is a new column with the difference from the first value
        df['computedTimeDays'] = (df_subset['date'] - givenOnset).dt.days
    # delete 'onset', 'date' columns (or keep them?)
    df = df[['personHash', 'computedTimeDays', 'viralLoad', 'age']]

    # Rename columns to match schema: 
    df = df.rename(columns={
        "personHash": "PersonID",
        "computedTimeDays": "TimeDays" 
        "viralLoad": "PathogenLoad", 
        "age": "AgeRng1"
        })

    # Add additional columns with known but missing information:
    df["StudyID"] = "jones2021"
    df["Pathogen"] = "SARS2"
    df["IndSpecies"] = "Human"
    df["Units"] = "GEml (log10VL)" # intercepts available in supplemental material
    df["DOI"] = "10.1126/science.abi5273"

    df = enforce_schema(df)
    df = coerce_types(df)
    return df