import pandas as pd
from schema import enforce_schema, coerce_types

def load_and_format():
    # Import the raw data:
    df = pd.read_csv("data/wagstaffe2024.csv")

    # Keep only the columns we need (all in this case): 
    df = df[['PersonID', 'DaysPostInoculation', 'GEml', 'site']]
    # for each individual we have 1 to 19.5 DaysPostInoculation data points with corresponding GEml (NA if not available)
    # Virological assessments of infections were based on 12-­ hour mid-turbinate and throat flocked swabs

    # Map the contents of column site (to be SampleType) to standard names: 
    df["site"] = df["site"].replace({
        "nose": "nasal",
        "throat": "throat" # need to confirm vs oropharyngeal -> see issue
        })

    # Rename columns to match schema: 
    df = df.rename(columns={
        "PersonID": "PersonID",
        "DaysPostInoculation": "TimeDays",
        "GEml": "Log10VL", # is this log10?
        "site": "SampleType"
        })

    # Add additional columns with known but missing information:
    df["StudyID"] = "wagstaffe2024"
    df["Pathogen"] = "SARS2"
    df["PtSpecies"] = "Human"
    df["DOI"] = "10.1126/sciimmunol.adj9285"
    df["Units"] = "GEml"

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

    df = enforce_schema(df)
    df = coerce_types(df)
    return df