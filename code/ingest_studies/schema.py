import pandas as pd

STANDARD_SCHEMA = [
    "StudyID", "PersonID", "InfectionID", "SampleID", "TimeDays",
    "Symptoms1", "Symptoms2", "Symptoms3", "Symptoms4",
    "Comorbidity1", "Comorbidity2", "Comorbidity3", "Comorbidity4",
    "Treatment1", "Treatment2", "Treatment3", "Treatment4",
    "Hospitalized", "SampleType", "AgeRng1", "AgeRng2",
    "Subtype", "Platform", "DOI", "Log10VL", "Units", "GEml_conversion_intercept", "GEml_conversion_slope"
]

def enforce_schema(df):
    """Add missing columns from the schema and return ordered DataFrame."""
    for col in STANDARD_SCHEMA:
        if col not in df.columns:
            df[col] = pd.NA
    return df[STANDARD_SCHEMA]

def coerce_types(df):
    numeric_cols = ["TimeDays", "AgeRng1", "AgeRng2", "GEml_conversion_intercept", "GEml_conversion_slope"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    string_cols = ["StudyID", "PersonID", "InfectionID", "SampleID", "Symptoms1", "Symptoms2", "Symptoms3", "Symptoms4", "Comorbidity1", "Comorbidity2", "Comorbidity3", "Comorbidity4", "Treatment1", "Treatment2", "Treatment3", "Treatment4", "SampleType", "Subtype", "Platform", "DOI", "Units"]
    df[string_cols] = df[string_cols].astype(str)

    return df

import pandas as pd

def split_age_range(df, col="AgeGrp", out1="AgeRng1", out2="AgeRng2"):
    """
    Splits an age range string like '[30, 39)' or '30-39' in a DataFrame column
    into two new numeric columns.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the age range column.
        col (str): Name of the column with age ranges.
        out1 (str): Name of the output column for the lower age bound.
        out2 (str): Name of the output column for the upper age bound.

    Returns:
        pd.DataFrame: A copy of the DataFrame with the new age range columns added.
    """
    df = df.copy()
    
    # Try different common formats: "[30, 39)", "30-39", "30 to 39"
    patterns = [
        r"[\[\(](\d+),\s*(\d+)[\)\]]",  # Matches [30, 39) or (30, 39]
        r"(\d+)[\s\-–to]+(\d+)",         # Matches 30-39, 30–39, 30 to 39
    ]
    
    for pattern in patterns:
        matches = df[col].str.extract(pattern)
        if matches.notna().all(axis=1).any():
            df[[out1, out2]] = matches
            break

    df[out1] = pd.to_numeric(df[out1], errors="coerce")
    df[out2] = pd.to_numeric(df[out2], errors="coerce")
    
    return df



