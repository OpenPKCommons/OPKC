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
    df = df[['personHash', 'onset', 'B117', 'date', 'viralLoad', 'age']] # redo patient ID to numerical instead of alphabetical - needed?

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
    df = df[['personHash', 'computedTimeDays', 'viralLoad', 'age', 'B117']]

    # Rename columns to match schema: 
    df = df.rename(columns={
        "personHash": "PersonID",
        "computedTimeDays": "TimeDays",
        "viralLoad": "PathogenLoad", 
        "age": "AgeRng1"
        })
    
    # for rows where "B117" is TRUE, df["Subtype"] = "B.1.1.7", else leave blank
    df["Subtype"] = ""
    df.loc[df["B117"] == True, "Subtype"] = "B.1.1.7"

    #and for thoes rows where df["Subtype"] == "B.1.1.7", df["Targets"] = "N501Y, del69/70 spike protein AA"
    df["Targets"] = ""
    df.loc[df["Subtype"] == "B.1.1.7", "Targets"] = "N501Y, del69/70 spike protein AA"

    # Add additional columns with known but missing information:
    df["StudyID"] = "jones2021"
    df["Pathogen"] = "SARS2"
    df["IndSpecies"] = "Human"
    df["Units"] = "GEml (log10VL)" # intercepts available in supplemental material
    df["DOI"] = "10.1126/science.abi5273"
    df["PlatformType"] = "RT-qPCR"
    # note that in data/jones2021_rawfiles, empirical culture data is recorded, confusingly labeled as "probabiliity"
    ## these were used to calculate the culture probability in the source paper, they are not simulated data
    ## not currently ingested here but could be added in future versions
    df["PlatformTech"] = "Roche Light Cycler 480, or Roche cobas 6800/8800"


    df = enforce_schema(df)
    df = coerce_types(df)
    return df