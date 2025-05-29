import pandas as pd
from schema import enforce_schema, coerce_types

def load_and_format():
    # Import the raw data:
    df = pd.read_csv("data/kissler2023.csv")

    # Keep only the columns we need: 
    df = df[['PersonID', 'InfectionEvent', 'TestDateIndex', 'CtT1', 'AgeGrp', 'LineageBroad']]

    # Format the age group column into separate age ranges: 
    df[["AgeRng1", "AgeRng2"]] = df["AgeGrp"].str.extract(r"[\[\(](\d+),\s*(\d+)[\)\]]")

    # Convert to numeric
    df["AgeRng1"] = pd.to_numeric(df["AgeRng1"], errors="coerce")
    df["AgeRng2"] = pd.to_numeric(df["AgeRng2"], errors="coerce")

    # Rename columns to match schema: 
    df = df.rename(columns={
        "InfectionEvent": "InfectionID",
        "TestDateIndex": "TimeDays",
        "CtT1": "Log10VL",
        "LineageBroad": "Subtype"
        })

    # Add additional columns with known but missing information:
    df["StudyID"] = "kissler2023"
    df["DOI"] = "10.1038/s41467-023-41941-z"
    df["Units"] = "Ct"
    df["Platform"] = "cobas_target1"
    df["GEml_conversion_intercept"] = 11.34089
    df["GEml_conversion_slope"] = -0.2770306
    df["SampleType"] = "nasal_oropharyngeal"

    df = enforce_schema(df)
    df = coerce_types(df)
    return df